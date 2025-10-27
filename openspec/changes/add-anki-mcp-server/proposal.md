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
