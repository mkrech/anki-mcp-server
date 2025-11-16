# Anki MCP Server

A Model Context Protocol (MCP) server that enables LLMs to interact with Anki flashcard software through AnkiConnect.

## Features

### Tools

- `list_decks` - List all available Anki decks
- `create_deck` - Create a new Anki deck
- `create_note` - Create a new note (Basic or Cloze)
- `batch_create_notes` - Create multiple notes at once
- `search_notes` - Search for notes using Anki query syntax
- `get_note_info` - Get detailed information about a note
- `update_note` - Update an existing note
- `delete_note` - Delete a note
- `list_note_types` - List all available note types
- `create_note_type` - Create a new note type
- `get_note_type_info` - Get detailed structure of a note type

### Resources

- `anki://decks/all` - Complete list of available decks
- `anki://note-types/all` - List of all available note types
- `anki://note-types/all-with-schemas` - Detailed structure information for all note types
- `anki://note-types/{modelName}` - Detailed structure information for a specific note type

## Prerequisites

1. [Anki](https://apps.ankiweb.net/) installed and running
2. [AnkiConnect](https://ankiweb.net/shared/info/2055492159) add-on installed in Anki

## Installation

### Development Installation

```bash
# Clone the repository
git clone <repository-url>
cd anki-tutor

# Create virtual environment and install
uv venv
uv pip install -e ".[dev]"
```

### Usage with Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "anki": {
      "command": "uv",
      "args": ["run", "anki-mcp-server"]
    }
  }
}
```

#### Using Custom AnkiConnect Port

```json
{
  "mcpServers": {
    "anki": {
      "command": "uv",
      "args": ["run", "anki-mcp-server", "--port", "8080"]
    }
  }
}
```

## Usage Examples

### Create a Basic Card

```
"Create an Anki card in the 'Default' deck:
Front: What is the capital of France?
Back: Paris"
```

### Create a Cloze Card

```
"Create a cloze card in the 'Programming' deck:
In Python, {{c1::list comprehensions}} provide a concise way to create {{c2::lists}}."
```

### Batch Create Cards

```
"Create 5 vocabulary cards for Spanish in the 'Spanish' deck from this list:
- hello: hola
- goodbye: adiós
- thank you: gracias
- please: por favor
- you're welcome: de nada"
```

## Workflow: PDF to Anki Pipeline

This project supports a complete pipeline for converting educational PDFs into Anki flashcards:

### Phase 1: PDF Processing

```
PDF → Docling Raw JSON → Intermediate JSON
```

**Step 1: Convert PDF to Docling Raw**
- Uses Docling DocumentConverter to extract document structure
- Preserves sections, tables, images, formulas, and hierarchy
- Output: `*_docling.json` and `*_docling.md` files
- Location: `data/input/intermediate/docling_raw/`

**Step 2: Convert to Intermediate Format**
- Transforms Docling output into structured sections
- Extracts hierarchy, metadata, and content relationships
- Output: `*.json` files with standardized structure
- Location: `data/input/intermediate/`

### Phase 2: Flashcard Generation & Import

```
Intermediate JSON → LLM via MCP → Anki (via AnkiConnect)
```

**Step 3: Generate Flashcards via LLM**

The LLM analyzes intermediate JSON content and generates flashcards with a proven distribution:
- **55% Cloze cards** - Fill-in-the-blank for definitions, formulas, concepts
- **30% KPRIM cards** - Four statements with True/False evaluation
- **10% Multiple Choice** - Multiple correct answers possible
- **5% Single Choice** - One correct answer

**Step 4: Batch Import to Anki**
- Create deck structure via `create_deck` tool
- Import cards in batches of 10-12 via `batch_create_notes`
- Use `allow_duplicate=true` parameter when encountering similar cards
- Generate import report in `data/progress/` directory

### Complete Example

```
1. Source: data/input/pdfs/pgm/exams/midterm-exam.pdf
   
2. Convert to Docling Raw:
   → data/input/intermediate/docling_raw/midterm-exam_docling.json
   → data/input/intermediate/docling_raw/midterm-exam_docling.md
   
3. Convert to Intermediate:
   → data/input/intermediate/midterm-exam.json
   
4. Generate & Import:
   → LLM analyzes content
   → Generates 50 cards (28 Cloze, 15 KPRIM, 5 MC, 2 SC)
   → Creates deck: PGM::MidtermExam
   → Imports in 5 batches (10-12 cards each)
   
5. Report:
   → data/progress/midterm-exam-import-report.md
```

### Best Practices

**Batch Import Strategy:**
- Process 10-12 cards per batch for optimal reliability
- Monitor success rates and adjust if needed
- Use `allow_duplicate=true` for KPRIM cards with similar patterns

**Quality Tracking:**
- Generate detailed import reports after each session
- Track card distribution, coverage, and success rates
- Store reports in `data/progress/` for reference

**Card Distribution:**
- Maintain 55/30/10/5 split for comprehensive learning
- Balance theoretical knowledge (Cloze) with application (KPRIM/MC/SC)
- Cover all major topics from source material

## Development

### Running Tests

```bash
pytest
```

### Code Quality

```bash
# Format code
ruff format .

# Lint code
ruff check .

# Auto-fix issues
ruff check --fix .
```

### Running Locally

```bash
# Default port (8765)
uv run anki-mcp-server

# Custom port
uv run anki-mcp-server --port 8080

# With debug logging
uv run anki-mcp-server --log-level DEBUG
```

## Architecture

- `client.py` - AnkiConnect API wrapper (anti-corruption layer)
- `tools.py` - MCP tool handlers for all Anki operations
- `resources.py` - MCP resource handlers with caching
- `server.py` - Main MCP server implementation
- `__main__.py` - CLI entry point

## Troubleshooting

### "Failed to connect to Anki"

1. Ensure Anki is running
2. Verify AnkiConnect add-on is installed
3. Check AnkiConnect is listening on the correct port (default: 8765)
4. Restart Anki and try again

### "Deck not found"

- Create the deck manually in Anki first, or
- Use the `create_deck` tool before creating notes

### "Note type not found"

- Use `list_note_types` to see available types
- Use `get_note_type_info` to see required fields
- Ensure field names match exactly (case-sensitive)

## License

MIT License
