# Project Context

## Purpose
Build an Anki MCP (Model Context Protocol) server that enables LLMs to interact with Anki flashcard software through AnkiConnect, providing the same functionality as the reference implementation at https://github.com/nailuoGG/anki-mcp-server.

## Tech Stack
- Python 3.13
- uv (package manager and build tool)
- ruff (linting and formatting)
- FASTMCP SDK for Python
- AnkiConnect (external Anki add-on)

## Project Conventions

### Code Style
- Use ruff for formatting and linting
- Follow PEP 8 conventions
- Type hints required for all public APIs
- Docstrings in Google style format
- Maximum line length: 100 characters

### Architecture Patterns
- Separate concerns: tools, resources, client, server
- Handler pattern for MCP operations
- Anti-corruption layer for AnkiConnect API
- Error handling with MCP error types
- Resource caching with expiry

### Testing Strategy
- Unit tests for all handlers
- Integration tests with mock AnkiConnect
- Test coverage minimum: 80%
- Use pytest as test framework

### Git Workflow
- Conventional commits
- Feature branches from main
- Squash and merge to main
- Tag releases with semantic versioning

## Domain Context
- **Anki**: Spaced repetition flashcard software
- **AnkiConnect**: Anki add-on providing HTTP API
- **MCP**: Model Context Protocol for LLM-tool integration
- **Note Types**: Templates defining card structure (Basic, Cloze, custom)
- **Decks**: Organizational containers for cards
- **Notes**: Content instances of note types

## Important Constraints
- Must maintain compatibility with AnkiConnect API
- Anki must be running for operations to work
- stdio-based MCP communication only
- No state persistence in MCP server (Anki is source of truth)

## External Dependencies
- AnkiConnect add-on running in Anki desktop application
- Default port: 8765 (configurable)
