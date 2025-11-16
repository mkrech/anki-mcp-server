# Anki MCP Server - Project Context

## Project Overview

This is an MCP (Model Context Protocol) server that enables LLMs to interact with Anki flashcard software. It provides a complete pipeline from educational PDFs to structured Anki flashcards.

## Current State (November 2025)

### Production Status
- ✅ Core MCP server fully operational
- ✅ 200+ flashcards successfully imported across 4 assignments
- ✅ Complete PDF processing pipeline validated
- ✅ 100% import success rate maintained

### Successfully Completed Imports
1. **Homework-3**: 50 cards → `PGM::Homework3` deck
2. **Homework-4**: 50 cards → `PGM::Homework4` deck
3. **Homework-5**: 50 cards → `PGM::Homework5` deck (Structure Learning, HMM, Markov Processes)
4. **Midterm-Exam**: 50 cards → `PGM::MidtermExam` deck (9 exam questions covering Chain Rule, Bayes, CI, d-separation, Junction Trees, EM)

## Complete Workflow Pipeline

### Phase 1: PDF Processing
```
PDF → Docling Raw JSON → Intermediate JSON
```

1. **PDF to Docling Raw** (via Docling MCP)
   - Input: `data/input/pdfs/pgm/**/*.pdf`
   - Output: `data/input/intermediate/docling_raw/*_docling.json` + `.md`
   - Preserves structure, tables, images, formulas

2. **Docling Raw to Intermediate**
   - Input: `data/input/intermediate/docling_raw/*_docling.json`
   - Output: `data/input/intermediate/*.json`
   - Structured sections with hierarchy and metadata

### Phase 2: Flashcard Generation & Import
```
Intermediate JSON → LLM/MCP → Anki (via AnkiConnect)
```

3. **LLM Analysis & Card Generation**
   - Analyze intermediate JSON content
   - Identify key concepts, definitions, relationships
   - Generate cards following standard distribution

4. **Batch Import to Anki**
   - Create deck via `mcp_anki_create_deck`
   - Import in batches via `mcp_anki_batch_create_notes`
   - Track progress and generate reports

## Standard Card Distribution

**Proven ratio for comprehensive learning:**
- **55% Cloze cards (28 of 50)** - Fill-in-the-blank for definitions, formulas, concepts
- **30% KPRIM cards (15 of 50)** - Four statements with True/False evaluation
- **10% Multiple Choice (5 of 50)** - Multiple correct answers possible
- **5% Single Choice (2 of 50)** - Single correct answer

## Batch Import Strategy

### Best Practices
- **Batch size**: 10-12 cards per batch (optimal for API reliability)
- **Duplicate handling**: Use `allow_duplicate=true` for KPRIM cards with similar patterns
- **Progress tracking**: Update after each batch completion
- **Error recovery**: Retry failed batches with adjusted parameters

### Typical Import Structure
```
Batch 1: 10 Cloze
Batch 2: 10 Cloze
Batch 3: 8 Cloze
Batch 4: 10 KPRIM
Batch 5: 12 cards (5 KPRIM + 5 MC + 2 SC)
```

## Key Files & Directories

### Source Code
- `src/anki_mcp_server/tools.py` - MCP tool handlers for Anki operations
- `src/anki_mcp_server/client.py` - AnkiConnect API wrapper (anti-corruption layer)
- `src/anki_mcp_server/server.py` - Main MCP server implementation
- `src/anki_mcp_server/server_fastmcp.py` - FastMCP server with Docling integration
- `src/anki_mcp_server/resources.py` - MCP resources for Anki metadata

### Data Structure
- `data/input/pdfs/pgm/` - Source PDF files (homework, exams, lectures)
- `data/input/intermediate/docling_raw/` - Docling raw JSON + Markdown outputs
- `data/input/intermediate/*.json` - Structured intermediate JSON files
- `data/progress/` - Import reports and tracking documents
- `data/sessions/` - Session data (if needed)

### Documentation
- `README.md` - Main documentation with workflow guide
- `AGENTS.md` - Instructions for AI agents
- `openspec/` - OpenSpec project structure and archived proposals
- `.github/prompts/` - Reusable prompt templates

## Anki Note Types

### Used in Production
1. **Cloze** - Standard Anki cloze deletion type
   - Fields: `Text`, `Back Extra`
   - Syntax: `{{c1::answer}}` for deletions

2. **AllInOne (kprim, mc, sc)** - Multi-purpose note type
   - KPRIM: 4 statements, each True/False
   - Multiple Choice: 4 options, multiple correct
   - Single Choice: 4 options, one correct
   - Fields: `Question`, `Statement1-4`, `Answer1-4`, `Extra`, `Tags`

## MCP Tools Reference

### Anki Tools (via AnkiConnect)
- `mcp_anki_create_deck` - Create new deck
- `mcp_anki_batch_create_notes` - Import 10-12 cards at once
- `mcp_anki_create_note` - Single card import (for corrections)
- `mcp_anki_search_notes` - Query existing cards
- `mcp_anki_list_decks` - List all decks
- `mcp_anki_list_note_types` - List available note types

### Docling Tools (via Docling MCP)
- `mcp_docling_convert_document_into_docling_document` - PDF to Docling Raw
- `mcp_anki_convert_pdf_to_docling_raw` - Direct PDF conversion
- `mcp_anki_convert_docling_raw_to_intermediate` - Raw to Intermediate

## Standards & Conventions

### Import Process
1. Always analyze source content first (identify topics, structure)
2. Identify relevant background lectures if available
3. Create deck with proper naming: `Subject::Assignment`
4. Generate cards following 55/30/10/5 distribution
5. Import in 5 batches (10, 10, 8, 10, 12 cards)
6. Use `allow_duplicate=true` for KPRIM batches if needed
7. Generate import report in `data/progress/`

### Card Quality Guidelines
- **Cloze**: Focus on definitions, formulas, key concepts
- **KPRIM**: Test understanding with multiple related statements
- **MC/SC**: Application-focused, realistic scenarios
- **Tags**: Use consistent tagging (e.g., `midterm`, `homework-5`, `hmm`, `d-separation`)
- **LaTeX**: Use KaTeX format for mathematical notation

### Import Reports
Generate after each complete import with:
- Total cards and success rate
- Distribution breakdown
- Topic coverage
- Batch details with Note IDs
- Quality metrics

## Common Issues & Solutions

### Duplicate Detection
**Problem**: `"cannot create note because it is a duplicate"`
**Solution**: Retry batch with `allow_duplicate=true`

### Batch Size
**Problem**: Timeouts or partial imports
**Solution**: Use 10-12 cards per batch, avoid larger batches

### Missing Decks
**Problem**: Deck not found error
**Solution**: Create deck first with `mcp_anki_create_deck` before importing cards

## Next Steps & Workflow

When user requests flashcard generation:

1. **Analyze source**: Read intermediate JSON, identify structure
2. **Check background**: Look for relevant lecture materials
3. **Create deck**: Use descriptive name with `::` hierarchy
4. **Generate cards**: Follow 55/30/10/5 distribution
5. **Import batches**: 5 batches of 10-12 cards each
6. **Generate report**: Create detailed import report in `data/progress/`
7. **Confirm completion**: Provide summary with deck ID and stats

## Project Metadata

- **Language**: Python 3.11+
- **Package Manager**: uv
- **MCP SDK**: Model Context Protocol
- **Anki Integration**: AnkiConnect add-on
- **Document Processing**: Docling
- **Testing**: pytest, ruff
- **License**: MIT
