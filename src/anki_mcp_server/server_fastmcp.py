"""Anki MCP Server implementation with FastMCP."""

import json
import logging
from pathlib import Path
from typing import Any

from docling.document_converter import DocumentConverter
from fastmcp import FastMCP
from mcp.types import TextContent

from anki_mcp_server.client import AnkiClient, AnkiConnectError

logger = logging.getLogger(__name__)

# Create FastMCP server
mcp = FastMCP("anki-mcp-server")

# Global client instance
_client: AnkiClient | None = None


def get_client() -> AnkiClient:
    """Get or create the global AnkiClient instance."""
    global _client
    if _client is None:
        _client = AnkiClient()
    return _client


async def check_anki_connection():
    """Check if Anki is running and available."""
    try:
        await get_client().check_connection()
    except AnkiConnectError as e:
        raise RuntimeError(
            f"Failed to connect to Anki: {e}\n"
            "Please ensure:\n"
            "1. Anki is running\n"
            "2. AnkiConnect add-on is installed\n"
            "3. AnkiConnect is listening on port 8765"
        ) from e


# Deck Management Tools


@mcp.tool()
async def list_decks() -> str:
    """List all available Anki decks.

    Returns:
        JSON string with list of deck names and count
    """
    await check_anki_connection()
    client = get_client()
    decks = await client.get_deck_names()
    import json

    return json.dumps({"decks": decks, "count": len(decks)}, indent=2)


@mcp.tool()
async def create_deck(name: str) -> str:
    """Create a new Anki deck.

    Args:
        name: Name of the deck to create (can include :: for nesting)

    Returns:
        JSON string with success status and deck ID
    """
    await check_anki_connection()
    client = get_client()
    deck_id = await client.create_deck(name)
    import json

    return json.dumps({"success": True, "deckId": deck_id}, indent=2)


# Note Type Management Tools


@mcp.tool()
async def list_note_types() -> str:
    """List all available note types.

    Returns:
        JSON string with list of note type names and count
    """
    await check_anki_connection()
    client = get_client()
    note_types = await client.get_model_names()
    import json

    return json.dumps({"noteTypes": note_types, "count": len(note_types)}, indent=2)


@mcp.tool()
async def get_note_type_info(model_name: str, include_css: bool = False) -> str:
    """Get detailed structure of a note type.

    Args:
        model_name: Name of the note type/model
        include_css: Whether to include CSS styling information

    Returns:
        JSON string with note type structure (fields, templates, css)
    """
    await check_anki_connection()
    client = get_client()

    fields = await client.get_model_field_names(model_name)
    templates = await client.get_model_templates(model_name)

    result: dict[str, Any] = {"modelName": model_name, "fields": fields, "templates": templates}

    if include_css:
        styling = await client.get_model_styling(model_name)
        result["css"] = styling.get("css", "")

    import json

    return json.dumps(result, indent=2)


@mcp.tool()
async def create_note_type(
    name: str, fields: list[str], templates: list[dict[str, str]], css: str = ""
) -> str:
    """Create a new note type.

    Args:
        name: Name of the new note type
        fields: List of field names
        templates: List of card templates with 'name', 'front', 'back' keys
        css: Optional CSS styling

    Returns:
        JSON string with success status and model info
    """
    await check_anki_connection()
    client = get_client()

    card_templates = [
        {"Name": t["name"], "Front": t["front"], "Back": t["back"]} for t in templates
    ]

    result = await client.create_model(name, fields, css, card_templates)
    import json

    return json.dumps({"success": True, "model": result}, indent=2)


# Note Management Tools


@mcp.tool()
async def create_note(
    note_type: str,
    deck: str,
    fields: dict[str, str],
    tags: list[str] | None = None,
    allow_duplicate: bool = False,
) -> str:
    """Create a single note in Anki.

    Args:
        note_type: Note type name (e.g., 'Basic', 'Cloze')
        deck: Target deck name
        fields: Dictionary of field names to values
        tags: Optional list of tags
        allow_duplicate: Whether to allow duplicate notes

    Returns:
        JSON string with success status and note ID
    """
    await check_anki_connection()
    client = get_client()

    note = {
        "deckName": deck,
        "modelName": note_type,
        "fields": fields,
        "tags": tags or [],
        "options": {"allowDuplicate": allow_duplicate},
    }

    note_id = await client.add_note(note)
    import json

    return json.dumps({"success": True, "noteId": note_id}, indent=2)


@mcp.tool()
async def batch_create_notes(
    notes: list[dict[str, Any]], allow_duplicate: bool = False, stop_on_error: bool = False
) -> str:
    """Create multiple notes at once (recommended: 10-20 notes per batch, max: 50).

    Args:
        notes: List of note dictionaries with 'type', 'deck', 'fields', optional 'tags'
        allow_duplicate: Whether to allow duplicate notes
        stop_on_error: Whether to stop on first error

    Returns:
        JSON string with results for each note
    """
    await check_anki_connection()
    client = get_client()

    if len(notes) > 50:
        raise ValueError("Maximum 50 notes per batch")

    note_data = []
    for note in notes:
        note_data.append(
            {
                "deckName": note["deck"],
                "modelName": note["type"],
                "fields": note["fields"],
                "tags": note.get("tags", []),
                "options": {"allowDuplicate": allow_duplicate},
            }
        )

    note_ids = await client.add_notes(note_data)

    results = []
    for i, note_id in enumerate(note_ids):
        if note_id is None:
            results.append({"index": i, "success": False, "error": "Failed to create note"})
            if stop_on_error:
                break
        else:
            results.append({"index": i, "success": True, "noteId": note_id})

    import json

    return json.dumps({"results": results, "total": len(results)}, indent=2)


@mcp.tool()
async def search_notes(query: str) -> str:
    """Search for notes using Anki query syntax.

    Args:
        query: Anki search query string

    Returns:
        JSON string with matching notes (up to 50) and total count
    """
    await check_anki_connection()
    client = get_client()

    note_ids = await client.find_notes(query)

    notes = []
    if note_ids:
        limit = min(len(note_ids), 50)
        notes_info = await client.notes_info(note_ids[:limit])
        notes = notes_info

    import json

    return json.dumps(
        {
            "query": query,
            "total": len(note_ids),
            "notes": notes,
            "limitApplied": len(note_ids) > 50,
        },
        indent=2,
    )


@mcp.tool()
async def get_note_info(noteId: int) -> str:
    """Get detailed information about a specific note.

    Args:
        noteId: Note ID

    Returns:
        JSON string with complete note details
    """
    await check_anki_connection()
    client = get_client()

    notes_info = await client.notes_info([noteId])
    if not notes_info:
        raise ValueError(f"Note not found: {noteId}")

    import json

    return json.dumps(notes_info[0], indent=2)


@mcp.tool()
async def update_note(id: int, fields: dict[str, str], tags: list[str] | None = None) -> str:
    """Update an existing note.

    Args:
        id: Note ID
        fields: Dictionary of field names to new values
        tags: Optional new tags (replaces all existing tags)

    Returns:
        JSON string with success status
    """
    await check_anki_connection()
    client = get_client()

    await client.update_note_fields(id, fields)

    if tags is not None:
        await client.update_note_tags(id, tags)

    import json

    return json.dumps({"success": True, "noteId": id}, indent=2)


@mcp.tool()
async def delete_note(id: int) -> str:
    """Delete a note permanently.

    Args:
        id: Note ID to delete

    Returns:
        JSON string with success status
    """
    await check_anki_connection()
    client = get_client()

    await client.delete_notes([id])
    import json

    return json.dumps({"success": True, "noteId": id}, indent=2)


# Resources


@mcp.resource("anki://decks/all")
async def get_all_decks() -> str:
    """Get all available Anki decks."""
    await check_anki_connection()
    client = get_client()
    decks = await client.get_deck_names()
    import json

    return json.dumps({"decks": decks, "count": len(decks)}, indent=2)


@mcp.resource("anki://note-types/all")
async def get_all_note_types() -> str:
    """Get all available note types."""
    await check_anki_connection()
    client = get_client()
    note_types = await client.get_model_names()
    import json

    return json.dumps({"noteTypes": note_types, "count": len(note_types)}, indent=2)


@mcp.resource("anki://note-types/{model_name}")
async def get_note_type_schema(model_name: str) -> str:
    """Get schema for a specific note type."""
    await check_anki_connection()
    client = get_client()

    fields = await client.get_model_field_names(model_name)
    templates = await client.get_model_templates(model_name)
    styling = await client.get_model_styling(model_name)

    return json.dumps(
        {
            "modelName": model_name,
            "fields": fields,
            "templates": templates,
            "css": styling.get("css", ""),
        },
        indent=2,
    )


# PDF Conversion Tools


async def _convert_pdf_to_docling_raw_impl(
    source: str,
    output_dir: str | None = None
) -> str:
    """Convert PDF to Docling raw JSON format.
    
    Internal implementation that performs the actual conversion.
    
    Args:
        source: Path to source PDF file
        output_dir: Output directory for Docling raw JSON files (defaults to ANKI_MCP_DOCLING_RAW_DIR env var)
        
    Returns:
        JSON string with conversion result and file paths
    """
    import os
    
    # Use environment variable if output_dir not provided
    if output_dir is None:
        output_dir = os.getenv("ANKI_MCP_DOCLING_RAW_DIR", "data/input/intermediate/docling_raw/")
    # Validate source exists
    source_path = Path(source)
    if not source_path.exists():
        return json.dumps({
            "success": False,
            "error": f"Source PDF not found: {source}"
        }, indent=2)
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    try:
        # Convert PDF using Docling
        converter = DocumentConverter()
        result = converter.convert(str(source_path))
        
        # Get the converted document
        doc = result.document
        
        # Generate output filenames
        basename = source_path.stem
        json_file = output_path / f"{basename}_docling.json"
        md_file = output_path / f"{basename}_docling.md"
        
        # Save as JSON
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(doc.export_to_dict(), f, indent=2, ensure_ascii=False)
        
        # Save as Markdown
        with open(md_file, "w", encoding="utf-8") as f:
            f.write(doc.export_to_markdown())
        
        return json.dumps({
            "success": True,
            "source": str(source_path),
            "json_file": str(json_file),
            "md_file": str(md_file),
            "message": f"Converted {source_path.name} to Docling format",
            "pages": len(doc.pages) if hasattr(doc, "pages") else None
        }, indent=2)
        
    except Exception as e:
        logger.error(f"Failed to convert PDF: {e}", exc_info=True)
        return json.dumps({
            "success": False,
            "error": str(e),
            "source": str(source)
        }, indent=2)


@mcp.tool()
async def convert_pdf_to_docling_raw(
    source: str,
    output_dir: str | None = None
) -> str:
    """Convert PDF to Docling raw JSON format.
    
    Uses Docling DocumentConverter to convert PDF directly to raw JSON and Markdown.
    Saves both formats to the output directory.
    
    Args:
        source: Path to source PDF file
        output_dir: Output directory for Docling raw JSON files (defaults to ANKI_MCP_DOCLING_RAW_DIR env var or data/input/intermediate/docling_raw/)
        
    Returns:
        JSON string with conversion result and file paths
    """
    return await _convert_pdf_to_docling_raw_impl(source, output_dir)


async def _convert_docling_raw_to_intermediate_impl(
    source: str,
    output_dir: str | None = None
) -> str:
    """Internal implementation for converting Docling raw to intermediate format."""
    import re
    import os
    
    # Use environment variable if output_dir not provided
    if output_dir is None:
        output_dir = os.getenv("ANKI_MCP_INTERMEDIATE_DIR", "data/input/intermediate/")
    
    # Validate source exists
    source_path = Path(source)
    if not source_path.exists():
        return json.dumps({
            "success": False,
            "error": f"Source file not found: {source}"
        }, indent=2)
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    try:
        # Load Docling raw JSON
        with open(source_path, 'r', encoding='utf-8') as f:
            docling_dict = json.load(f)
        
        # Extract basename
        base_name = source_path.stem.replace('_docling', '')
        
        # Extract sections
        sections = []
        texts = docling_dict.get('texts', [])
        header_indices = [i for i, t in enumerate(texts) if t.get('label') == 'section_header']
        
        if header_indices:
            # Standard processing with section headers
            current_section_id = 0
            
            for header_idx_pos, text_idx in enumerate(header_indices):
                text_item = texts[text_idx]
                
                level = text_item.get('level', 1)
                title = text_item.get('text', f"Section {current_section_id}")
                
                # Page number from prov
                prov = text_item.get('prov', [])
                page_num = prov[0].get('page_no', 1) if prov else 1
                
                # Content: collect text until next header
                next_header_idx = header_indices[header_idx_pos + 1] if header_idx_pos + 1 < len(header_indices) else len(texts)
                content_items = texts[text_idx + 1:next_header_idx]
                content = '\n\n'.join(item.get('text', '') for item in content_items if item.get('text'))
                
                section_id = f"{base_name}_sec_{current_section_id}"
                section = {
                    "id": section_id,
                    "title": title,
                    "content": content,
                    "level": level,
                    "page": page_num,
                    "parent_id": None,
                    "chapter": None,
                    "section_number": None,
                    "image_path": f"data/input/intermediate/slide_images/{base_name}/pgm_{base_name}_slide_{page_num}.png"
                }
                
                sections.append(section)
                current_section_id += 1
        else:
            # Fallback: single section with all content
            full_text = '\n\n'.join(item.get('text', '') for item in texts if item.get('text'))
            page_num = 1
            if texts and texts[0].get('prov'):
                page_num = texts[0]['prov'][0].get('page_no', 1)
            
            section = {
                "id": f"{base_name}_sec_0",
                "title": base_name,
                "content": full_text,
                "level": 1,
                "page": page_num,
                "parent_id": None,
                "chapter": None,
                "section_number": None,
                "image_path": f"data/input/intermediate/slide_images/{base_name}/pgm_{base_name}_slide_{page_num}.png"
            }
            sections.append(section)
        
        # Create structured document
        doc_dict = {
            "file_path": f"data/pdfs/{base_name}.pdf",
            "metadata": {
                "source": "docling",
                "docling_file": str(source_path),
                "base_name": base_name
            },
            "sections": sections,
            "tables": [],
            "stats": {
                "total_sections": len(sections),
                "total_tables": 0
            }
        }
        
        # Save structured JSON
        output_file = output_path / f"{base_name}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(doc_dict, f, indent=2, ensure_ascii=False)
        
        return json.dumps({
            "success": True,
            "source": str(source_path),
            "output_file": str(output_file),
            "sections": len(sections),
            "message": f"Converted {source_path.name} to structured format"
        }, indent=2)
        
    except Exception as e:
        logger.error(f"Failed to convert Docling raw to intermediate: {e}", exc_info=True)
        return json.dumps({
            "success": False,
            "error": str(e),
            "source": str(source)
        }, indent=2)


@mcp.tool()
async def convert_docling_raw_to_intermediate(
    source: str,
    output_dir: str | None = None
) -> str:
    """Convert Docling raw JSON to structured intermediate JSON format.
    
    Extracts sections, hierarchy, and metadata from Docling raw JSON and
    converts it to the structured format used for flashcard generation.
    
    Args:
        source: Path to Docling raw JSON file (*_docling.json)
        output_dir: Output directory for structured JSON files (defaults to ANKI_MCP_INTERMEDIATE_DIR env var or data/input/intermediate/)
        
    Returns:
        JSON string with conversion result and file paths
    """
    return await _convert_docling_raw_to_intermediate_impl(source, output_dir)
