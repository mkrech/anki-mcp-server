## Context

Building a Python-based MCP server to interface with Anki's AnkiConnect add-on. This is a greenfield project requiring careful architecture to ensure maintainability and alignment with MCP best practices while wrapping a third-party API.

**Stakeholders**: Developers using LLMs to create learning materials, AI assistants interacting with Anki.

**Constraints**:
- Must use Python (not TypeScript like reference implementation)
- AnkiConnect API is external, versioned separately
- stdio-only MCP communication (no HTTP)
- No state persistence (Anki is source of truth)

## Goals / Non-Goals

**Goals**:
- Feature parity with reference TypeScript implementation
- Idiomatic Python using modern tooling (uv, ruff)
- Clear separation of concerns (client, tools, resources, server)
- Robust error handling for network and Anki failures
- Performance optimization via caching and batch operations

**Non-Goals**:
- Replacing or extending AnkiConnect itself
- Supporting MCP transports other than stdio
- Implementing Anki's spaced repetition algorithm
- Building a GUI or web interface

## Decisions

### Decision 1: Package Structure
Use standard Python package with `src/` layout:
```
anki-mcp-server/
├── pyproject.toml
├── src/
│   └── anki_mcp_server/
│       ├── __init__.py
│       ├── __main__.py       # CLI entry point
│       ├── server.py          # MCP server class
│       ├── client.py          # AnkiConnect wrapper
│       ├── tools.py           # Tool handlers
│       └── resources.py       # Resource handlers
└── tests/
```

**Why**: Follows modern Python packaging conventions, clear module separation.

**Alternatives considered**:
- Flat structure: Rejected due to complexity with multiple handler classes
- Monolithic file: Rejected for maintainability

### Decision 2: AnkiConnect Client Wrapper
Create an anti-corruption layer class (`AnkiClient`) wrapping all AnkiConnect API calls.

**Why**: 
- Isolates external API changes
- Centralizes connection management and error handling
- Enables easier testing with mocks

**Implementation**:
```python
class AnkiClient:
    def __init__(self, url: str = "http://localhost:8765"):
        self.url = url
    
    async def check_connection(self) -> None:
        """Verify Anki is running."""
    
    async def get_deck_names(self) -> list[str]:
        """List all decks."""
    
    # ... other methods
```

### Decision 3: Tool and Resource Handlers
Separate handler classes for tools and resources following MCP SDK patterns.

**Why**:
- Clear responsibility separation
- Easier unit testing
- Aligns with reference implementation architecture

```python
class ToolHandler:
    def __init__(self, client: AnkiClient):
        self.client = client
    
    async def get_tool_schema(self) -> dict:
        """Return all tool definitions."""
    
    async def execute_tool(self, name: str, args: dict) -> dict:
        """Execute a tool by name."""

class ResourceHandler:
    def __init__(self, client: AnkiClient):
        self.client = client
        self._cache: dict = {}
        self._cache_expiry = 300  # 5 minutes
    
    async def list_resources(self) -> dict:
        """Return available resources."""
    
    async def read_resource(self, uri: str) -> dict:
        """Read a resource by URI."""
```

### Decision 4: Error Handling Strategy
Use MCP SDK error types and wrap AnkiConnect errors appropriately.

**Error mapping**:
- Network errors → `McpError(ErrorCode.InternalError, "Cannot connect to Anki")`
- Invalid parameters → `McpError(ErrorCode.InvalidParams, <details>)`
- Missing resources → `McpError(ErrorCode.InvalidParams, "Resource not found")`

**Why**: Standardizes error responses for MCP clients.

### Decision 5: Caching Strategy
Cache note type schemas with 5-minute TTL to reduce AnkiConnect calls.

**What to cache**:
- Note type definitions (fields, templates, CSS)
- All note types list

**What NOT to cache**:
- Deck lists (users may add decks frequently)
- Notes (content changes often)
- Search results

**Why**: Note types change rarely, schemas are requested frequently.

### Decision 6: Batch Operations
Recommend 10-20 notes per batch in documentation, enforce 50-note maximum.

**Why**: 
- Balances performance vs. error handling complexity
- Matches reference implementation recommendations
- Prevents timeouts on large batches

## Risks / Trade-offs

### Risk: AnkiConnect API Changes
**Mitigation**: 
- Version lock AnkiConnect requirements in documentation
- Client wrapper isolates changes to one module
- Add API version checking on startup

### Risk: Network Timeouts
**Mitigation**:
- Configurable timeout (default 30s)
- Retry logic with exponential backoff
- Clear error messages suggesting user check Anki is running

### Risk: Large Batch Operations
**Mitigation**:
- Document batch size recommendations
- Add `stopOnError` flag for batch operations
- Return partial success information

### Trade-off: Python vs TypeScript
**Chosen**: Python for user's requirement
**Cost**: Different ecosystem, async patterns differ slightly
**Benefit**: Broader Python ML/AI ecosystem integration

## Migration Plan

N/A - This is a new project with no existing users to migrate.

## Open Questions

- [ ] Should we support custom AnkiConnect installations with authentication?
  - **Decision pending**: Default assumes local unauthenticated AnkiConnect
- [ ] Should we publish to PyPI immediately or wait for beta testing?
  - **Decision pending**: Start with GitHub installation, PyPI after validation
- [ ] What level of logging should be default?
  - **Proposal**: Error-level to stderr, debug via environment variable
