"""Anki MCP Server implementation with FastMCP."""

import logging
from typing import Any

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

    import json

    return json.dumps(
        {
            "modelName": model_name,
            "fields": fields,
            "templates": templates,
            "css": styling.get("css", ""),
        },
        indent=2,
    )
