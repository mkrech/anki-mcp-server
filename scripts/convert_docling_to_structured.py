#!/usr/bin/env python3
"""
Konvertiert Docling Raw JSON zu strukturiertem Intermediate JSON.

Dieses Script liest die rohen Docling JSON-Dateien aus docling_raw/
und konvertiert sie in strukturierte HierarchicalDoc JSON-Dateien.

Input:  data/intermediate/docling_raw/*_docling.json
Output: data/intermediate/{filename}.json

Usage:
    # Einzelne Datei
    python scripts/convert_docling_to_structured.py data/intermediate/docling_raw/01_tud_PGM01_intro_docling.json
    
    # Ganzer Ordner
    python scripts/convert_docling_to_structured.py data/intermediate/docling_raw/
    
    # Mehrere Dateien
    python scripts/convert_docling_to_structured.py file1.json file2.json
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class Section:
    """Eine Section aus einem geparsten Dokument."""
    id: str
    title: str
    content: str
    level: int
    page: Optional[int] = None
    parent_id: Optional[str] = None
    chapter: Optional[str] = None
    section_number: Optional[str] = None
    content_de: Optional[str] = None
    image_path: Optional[str] = None


@dataclass
class HierarchicalDoc:
    """Ein komplett geparster PDF mit hierarchischer Struktur."""
    file_path: str
    sections: List[Section]
    tables: List[Dict] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class DoclingToStructuredConverter:
    """Konvertiert Docling Raw JSON zu strukturiertem Format."""
    
    def __init__(self, output_dir: str = "data/intermediate"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def convert_file(self, docling_json_path: str) -> Optional[str]:
        """
        Konvertiert eine einzelne Docling JSON-Datei.
        
        Args:
            docling_json_path: Pfad zur Docling JSON-Datei
            
        Returns:
            Pfad zur erstellten Intermediate JSON-Datei oder None bei Fehler
        """
        docling_path = Path(docling_json_path)
        
        if not docling_path.exists():
            print(f"❌ Datei nicht gefunden: {docling_json_path}")
            return None
        
        # Lade Docling JSON
        try:
            with open(docling_path, 'r', encoding='utf-8') as f:
                docling_dict = json.load(f)
        except Exception as e:
            print(f"❌ Fehler beim Laden von {docling_path.name}: {e}")
            return None
        
        # Extrahiere Basename (entferne _docling.json)
        base_name = docling_path.stem.replace('_docling', '')
        
        # Konstruiere PDF-Pfad (nur für Metadata)
        pdf_path = f"data/pdfs/{base_name}.pdf"
        
        print(f"\n📄 Konvertiere: {docling_path.name}")
        
        # Extrahiere Sections
        sections = self._extract_sections(docling_dict, pdf_path, str(docling_path))
        
        if not sections:
            print(f"  ⚠️  Keine Sections gefunden")
            return None
        
        print(f"  ✓ {len(sections)} Sections extrahiert")
        
        # Erstelle HierarchicalDoc
        doc = HierarchicalDoc(
            file_path=pdf_path,
            sections=sections,
            tables=[],  # Tables werden hier nicht verarbeitet
            metadata={
                "source": "docling",
                "docling_file": str(docling_path),
                "base_name": base_name
            }
        )
        
        # Speichere als strukturiertes JSON
        output_path = self.output_dir / f"{base_name}.json"
        self._save_doc(doc, output_path)
        
        print(f"  💾 Gespeichert: {output_path}")
        
        return str(output_path)
    
    def _extract_sections(self, docling_dict: Dict, pdf_path: str, docling_json_path: str) -> List[Section]:
        """
        Extrahiert Sections aus Docling JSON.
        
        Nutzt prov[0]['page_no'] für korrekte PDF-Seitennummern.
        """
        sections = []
        
        texts = docling_dict.get('texts', [])
        header_indices = [i for i, t in enumerate(texts) if t.get('label') == 'section_header']
        
        if not header_indices:
            # Fallback für PDFs ohne Headers
            return self._extract_sections_fallback(docling_dict, pdf_path)
        
        current_section_id = 0
        parent_stack = []
        current_chapter = None
        
        # Iteriere über Header
        for header_idx_pos, text_idx in enumerate(header_indices):
            text_item = texts[text_idx]
            
            level = text_item.get('level', 1)
            title = text_item.get('text', f"Section {current_section_id}")
            
            # Extrahiere Chapter und Section Number
            chapter, section_number = self._extract_chapter_info(title, level)
            
            if level == 1 and chapter:
                current_chapter = chapter
            
            # Parent-Stack aktualisieren
            while parent_stack and parent_stack[-1]['level'] >= level:
                parent_stack.pop()
            
            parent_id = parent_stack[-1]['id'] if parent_stack else None
            
            section_id = f"{Path(pdf_path).stem}_sec_{current_section_id}"
            
            # Page Number aus prov
            page_num = None
            prov = text_item.get('prov', [])
            if prov and len(prov) > 0:
                page_num = prov[0].get('page_no')
            
            # Image Path
            image_path = None
            if page_num:
                base_filename = Path(pdf_path).stem
                image_path = f"data/intermediate/slide_images/{base_filename}/pgm_{base_filename}_slide_{page_num}.png"
            
            # Content sammeln (Header + nachfolgende Texte)
            content_parts = [f"## {title}\n\n"]
            next_header_idx = header_indices[header_idx_pos + 1] if header_idx_pos + 1 < len(header_indices) else len(texts)
            
            for i in range(text_idx + 1, next_header_idx):
                item = texts[i]
                if item.get('label') == 'text':
                    text_content = item.get('text', '').strip()
                    if text_content:
                        content_parts.append(text_content)
            
            content = '\n'.join(content_parts)
            
            # Erstelle Section
            section = Section(
                id=section_id,
                title=title,
                content=content,
                level=level,
                page=page_num,
                parent_id=parent_id,
                chapter=chapter or current_chapter,
                section_number=section_number,
                image_path=image_path
            )
            
            sections.append(section)
            parent_stack.append({'id': section_id, 'level': level})
            current_section_id += 1
        
        return sections
    
    def _extract_sections_fallback(self, docling_dict: Dict, pdf_path: str) -> List[Section]:
        """
        Fallback für PDFs ohne section_header.
        Versucht nach Homework-Pattern oder ganzes Dokument.
        """
        sections = []
        base_filename = Path(pdf_path).stem
        texts = docling_dict.get('texts', [])
        
        # Sammle allen Text
        full_text = '\n'.join(item.get('text', '') for item in texts if item.get('text'))
        
        # Für Homework: Splitte nach Aufgaben-Nummern
        if 'homework' in base_filename.lower():
            pattern = r'^(\d+)\.\s+'
            splits = re.split(pattern, full_text, flags=re.MULTILINE)
            
            if len(splits) > 2:
                for i in range(1, len(splits), 2):
                    if i + 1 < len(splits):
                        task_num = splits[i]
                        task_text = splits[i + 1].strip()
                        
                        if task_text:
                            # Page Number suchen
                            page_num = 1
                            for item in texts:
                                if task_text[:50] in item.get('text', ''):
                                    prov = item.get('prov', [])
                                    if prov and 'page_no' in prov[0]:
                                        page_num = prov[0]['page_no']
                                        break
                            
                            image_path = f"data/intermediate/slide_images/{base_filename}/pgm_{base_filename}_slide_{page_num}.png"
                            
                            section = Section(
                                id=f"{base_filename}_sec_{i//2}",
                                title=f"{base_filename} - Task {task_num}",
                                content=f"## Task {task_num}\n\n{task_text}",
                                level=1,
                                page=page_num,
                                parent_id=None,
                                chapter=None,
                                section_number=int(task_num),
                                image_path=image_path
                            )
                            sections.append(section)
                
                return sections
        
        # Fallback: Ganzes Dokument als eine Section
        image_path = f"data/intermediate/slide_images/{base_filename}/pgm_{base_filename}_slide_1.png"
        section = Section(
            id=f"{base_filename}_sec_0",
            title=base_filename,
            content=full_text,
            level=1,
            page=1,
            parent_id=None,
            chapter=None,
            section_number=None,
            image_path=image_path
        )
        return [section]
    
    def _extract_chapter_info(self, title: str, level: int) -> Tuple[Optional[str], Optional[str]]:
        """
        Extrahiert Chapter und Section Number aus Titel.
        
        Patterns:
        - "Chapter 9" → chapter="9"
        - "9. Variable Elimination" → chapter="9"
        - "9.2 Inference" → chapter="9", section_number="9.2"
        """
        chapter = None
        section_number = None
        
        # Pattern 1: "Chapter X"
        match = re.match(r'^(?:Chapter|Kapitel)\s+(\d+)', title, re.IGNORECASE)
        if match:
            chapter = match.group(1)
            section_number = chapter
            return chapter, section_number
        
        # Pattern 2: "X.Y.Z Topic"
        match = re.match(r'^(\d+(?:\.\d+)*)\s+', title)
        if match:
            section_number = match.group(1)
            chapter = section_number.split('.')[0]
            return chapter, section_number
        
        # Pattern 3: "X. Topic" (nur bei Level 1)
        if level == 1:
            match = re.match(r'^(\d+)\.\s+', title)
            if match:
                chapter = match.group(1)
                section_number = chapter
                return chapter, section_number
        
        return None, None
    
    def _save_doc(self, doc: HierarchicalDoc, output_path: Path):
        """Speichert HierarchicalDoc als JSON."""
        doc_dict = {
            "file_path": doc.file_path,
            "metadata": doc.metadata,
            "sections": [
                {
                    "id": s.id,
                    "title": s.title,
                    "content": s.content,
                    "content_de": s.content_de,
                    "level": s.level,
                    "page": s.page,
                    "parent_id": s.parent_id,
                    "chapter": s.chapter,
                    "section_number": s.section_number,
                    "image_path": s.image_path
                }
                for s in doc.sections
            ],
            "tables": doc.tables,
            "stats": {
                "total_sections": len(doc.sections),
                "total_tables": len(doc.tables)
            }
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(doc_dict, f, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(
        description="Konvertiert Docling Raw JSON zu strukturiertem Format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Beispiele:
  # Einzelne Datei
  python scripts/convert_docling_to_structured.py data/intermediate/docling_raw/01_tud_PGM01_intro_docling.json
  
  # Ganzer Ordner
  python scripts/convert_docling_to_structured.py data/intermediate/docling_raw/
  
  # Mehrere Dateien
  python scripts/convert_docling_to_structured.py file1.json file2.json

Output:
  - data/intermediate/{filename}.json
        """
    )
    
    parser.add_argument(
        "sources",
        nargs="+",
        help="Docling JSON-Datei(en) oder Ordner"
    )
    
    parser.add_argument(
        "-o", "--output-dir",
        default="data/intermediate",
        help="Output-Verzeichnis (default: data/intermediate)"
    )
    
    args = parser.parse_args()
    
    # Sammle alle JSON-Dateien
    json_files = []
    for source in args.sources:
        source_path = Path(source)
        
        if source_path.is_file() and source_path.suffix == '.json':
            json_files.append(source_path)
        elif source_path.is_dir():
            # Sammle alle *_docling.json Dateien
            json_files.extend(source_path.glob('*_docling.json'))
        else:
            print(f"⚠️  Überspringe: {source} (keine JSON-Datei oder Ordner)")
    
    if not json_files:
        print("❌ Keine Docling JSON-Dateien gefunden!")
        sys.exit(1)
    
    print("=" * 60)
    print(f"🔄 DOCLING → STRUCTURED CONVERTER")
    print("=" * 60)
    print(f"📂 Input:  {len(json_files)} Dateien")
    print(f"📂 Output: {args.output_dir}")
    
    # Konvertiere alle Dateien
    converter = DoclingToStructuredConverter(output_dir=args.output_dir)
    
    converted = []
    failed = []
    
    for json_file in json_files:
        try:
            output_path = converter.convert_file(str(json_file))
            if output_path:
                converted.append(output_path)
            else:
                failed.append(str(json_file))
        except Exception as e:
            print(f"❌ Fehler bei {json_file.name}: {e}")
            failed.append(str(json_file))
    
    # Zusammenfassung
    print("\n" + "=" * 60)
    print("📊 ZUSAMMENFASSUNG")
    print("=" * 60)
    print(f"✓ Konvertiert: {len(converted)} Dateien")
    if failed:
        print(f"❌ Fehler:      {len(failed)} Dateien")
        for f in failed:
            print(f"   - {Path(f).name}")
    
    print("\n💡 NÄCHSTE SCHRITTE:")
    print("   1. Review JSON: cat data/intermediate/{filename}.json")
    print("   2. Erstelle Karten via Chat mit GitHub Copilot")
    print("   3. Parse: python scripts/parse_llm_cards.py")
    print("   4. Export: python scripts/export_to_csv.py")


if __name__ == "__main__":
    main()
