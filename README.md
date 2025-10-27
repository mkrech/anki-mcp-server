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
