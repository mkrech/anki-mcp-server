## 1. Project Setup
- [x] 1.1 Initialize Python project with uv (`pyproject.toml`, package structure)
- [x] 1.2 Configure ruff for linting and formatting
- [x] 1.3 Set up pytest with test structure
- [x] 1.4 Create package structure (`src/anki_mcp_server/`)
- [x] 1.5 Add MCP SDK dependency

## 2. Core Infrastructure
- [x] 2.1 Implement AnkiConnect client wrapper (`client.py`)
- [x] 2.2 Add connection checking and error handling
- [x] 2.3 Implement retry logic for network operations
- [x] 2.4 Create base MCP server class (`server.py`)
- [x] 2.5 Set up stdio transport

## 3. Deck Management Tools
- [x] 3.1 Implement `list_decks` tool
- [x] 3.2 Implement `create_deck` tool
- [x] 3.3 Add tool schemas and validation
- [x] 3.4 Write unit tests for deck operations

## 4. Note Type Management
- [x] 4.1 Implement `list_note_types` tool
- [x] 4.2 Implement `get_note_type_info` tool with field details
- [x] 4.3 Implement `create_note_type` tool
- [x] 4.4 Add support for custom templates and CSS
- [x] 4.5 Write unit tests for note type operations

## 5. Note Management Tools
- [x] 5.1 Implement `create_note` tool (Basic and Cloze)
- [x] 5.2 Implement `batch_create_notes` with batch size recommendations
- [x] 5.3 Implement `search_notes` with Anki query syntax
- [x] 5.4 Implement `get_note_info` tool
- [x] 5.5 Implement `update_note` tool
- [x] 5.6 Implement `delete_note` tool
- [x] 5.7 Add duplicate detection support
- [x] 5.8 Write unit tests for all note operations

## 6. MCP Resources
- [x] 6.1 Implement `anki://decks/all` resource
- [x] 6.2 Implement `anki://note-types/all` resource
- [x] 6.3 Implement `anki://note-types/all-with-schemas` resource
- [x] 6.4 Implement `anki://note-types/{modelName}` resource template
- [x] 6.5 Add resource caching with 5-minute expiry
- [x] 6.6 Write unit tests for resources

## 7. CLI and Entry Point
- [x] 7.1 Create CLI entry point (`__main__.py`)
- [x] 7.2 Add `--port` argument for custom AnkiConnect port
- [x] 7.3 Add proper error handling and logging
- [x] 7.4 Configure package console scripts

## 8. Documentation
- [x] 8.1 Write README with installation instructions
- [x] 8.2 Document all tools with examples
- [x] 8.3 Document all resources
- [x] 8.4 Add troubleshooting guide
- [x] 8.5 Create configuration examples for Claude Desktop and Cline

## 9. Testing and Quality
- [x] 9.1 Achieve 80% test coverage
- [x] 9.2 Add integration tests with mock AnkiConnect
- [x] 9.3 Test error scenarios (Anki not running, invalid input)
- [x] 9.4 Run ruff checks and fix all issues
- [x] 9.5 Validate with MCP Inspector

## 10. Deployment
- [x] 10.1 Create package build configuration
- [x] 10.2 Test local installation with `uv pip install -e .`
- [x] 10.3 Verify CLI works: `anki-mcp-server --help`
- [x] 10.4 Test with Claude Desktop configuration
- [x] 10.5 Real-world validation (200+ cards imported)

## 11. PDF to Anki Pipeline
- [x] 11.1 Integrate Docling MCP for PDF processing
- [x] 11.2 Implement Docling Raw JSON to Intermediate conversion
- [x] 11.3 Define standard card distribution (55/30/10/5)
- [x] 11.4 Establish batch import workflow (10-12 cards)
- [x] 11.5 Create import report template and generation
- [x] 11.6 Document complete pipeline in README
- [x] 11.7 Validate with multiple homework/exam imports

## 12. Production Validation
- [x] 12.1 Homework-3 import (50 cards, PGM::Homework3)
- [x] 12.2 Homework-4 import (50 cards, PGM::Homework4)
- [x] 12.3 Homework-5 import (50 cards, PGM::Homework5)
- [x] 12.4 Midterm-Exam import (50 cards, PGM::MidtermExam)
- [x] 12.5 Generate import reports for quality tracking
- [x] 12.6 Verify card distribution consistency
- [x] 12.7 Confirm 100% import success rate
