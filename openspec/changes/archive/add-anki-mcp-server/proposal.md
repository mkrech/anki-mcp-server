## Why

LLMs need a structured way to interact with Anki flashcard software to create, manage, and query flashcards programmatically. This enables AI assistants to help users build spaced repetition learning materials directly from conversations.

## What Changes

- Add new Python package `anki-mcp-server` with MCP server implementation
- Implement 11 MCP tools for deck and note management
- Implement 4 MCP resources for querying Anki metadata
- Provide AnkiConnect client wrapper as anti-corruption layer
- Support Basic and Cloze note types plus custom note types
- Enable batch operations for efficient note creation
- Include CLI with configurable AnkiConnect port

## Impact

- Affected specs: 
  - `deck-management` (new)
  - `note-management` (new)
  - `note-type-management` (new)
  - `anki-resources` (new)
- Affected code:
  - New package structure under project root
  - Python package with uv/ruff tooling
  - MCP SDK integration
  - AnkiConnect API integration

## Implementation Status

**Status:** ✅ COMPLETED

### Core Functionality (100%)
- ✅ AnkiConnect client wrapper with error handling
- ✅ MCP server with stdio transport
- ✅ 11 tools for deck, note, and note type management
- ✅ 4 resources for Anki metadata queries
- ✅ Batch operations with 10-12 card recommendations
- ✅ CLI with configurable port

### PDF to Anki Pipeline (100%)
- ✅ Docling integration for PDF processing
- ✅ Intermediate JSON format conversion
- ✅ LLM-driven flashcard generation workflow
- ✅ Batch import with progress tracking
- ✅ Import report generation

### Documentation (100%)
- ✅ README with installation and usage
- ✅ Tool and resource documentation
- ✅ Troubleshooting guide
- ✅ Claude Desktop configuration examples
- ✅ PDF to Anki workflow documentation

### Real-World Validation
Successfully generated and imported flashcards for:
- Homework-3: 50 cards (PGM::Homework3)
- Homework-4: 50 cards (PGM::Homework4)
- Homework-5: 50 cards (PGM::Homework5)
- Midterm-Exam: 50 cards (PGM::MidtermExam)

**Total:** 200+ cards imported with 100% success rate

### Proven Card Distribution
- 55% Cloze (definitions, formulas, concepts)
- 30% KPRIM (four-statement True/False evaluation)
- 10% Multiple Choice (multiple correct answers)
- 5% Single Choice (one correct answer)

### Key Achievements
- Batch import reliability (10-12 cards per batch)
- Quality tracking via import reports (`data/progress/`)
- Complete PDF → Docling → Intermediate → Anki pipeline
- Integration with Docling MCP for document processing
- Support for complex note types (AllInOne: KPRIM, MC, SC)
