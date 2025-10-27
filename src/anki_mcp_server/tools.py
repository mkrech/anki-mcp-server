"""MCP tool handlers for Anki operations."""

from typing import Any

from mcp.types import TextContent, Tool

from anki_mcp_server.client import AnkiClient


class ToolHandler:
    """Handles all MCP tool operations for Anki.

    Args:
        client: AnkiConnect client instance
    """

    def __init__(self, client: AnkiClient):
        self.client = client

    def get_tool_list(self) -> list[Tool]:
        """Return list of all available tools."""
        return [
            Tool(
                name="list_decks",
                description="List all available Anki decks",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": [],
                },
            ),
            Tool(
                name="create_deck",
                description="Create a new Anki deck",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Name of the deck to create",
                        }
                    },
                    "required": ["name"],
                },
            ),
            Tool(
                name="list_note_types",
                description="List all available note types",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": [],
                },
            ),
            Tool(
                name="get_note_type_info",
                description="Get detailed structure of a note type",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "modelName": {
                            "type": "string",
                            "description": "Name of the note type/model",
                        },
                        "includeCss": {
                            "type": "boolean",
                            "description": "Whether to include CSS information",
                        },
                    },
                    "required": ["modelName"],
                },
            ),
            Tool(
                name="create_note_type",
                description="Create a new note type",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Name of the new note type"},
                        "fields": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Field names for the note type",
                        },
                        "css": {"type": "string", "description": "CSS styling for the note type"},
                        "templates": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string"},
                                    "front": {"type": "string"},
                                    "back": {"type": "string"},
                                },
                                "required": ["name", "front", "back"],
                            },
                            "description": "Card templates",
                        },
                    },
                    "required": ["name", "fields", "templates"],
                },
            ),
            Tool(
                name="create_note",
                description="Create a single note",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "type": {
                            "type": "string",
                            "description": "Note type (e.g., 'Basic', 'Cloze')",
                        },
                        "deck": {"type": "string", "description": "Target deck name"},
                        "fields": {
                            "type": "object",
                            "description": "Note fields",
                            "additionalProperties": True,
                        },
                        "tags": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Optional tags",
                        },
                        "allowDuplicate": {
                            "type": "boolean",
                            "description": "Whether to allow duplicate notes",
                        },
                    },
                    "required": ["type", "deck", "fields"],
                },
            ),
            Tool(
                name="batch_create_notes",
                description="Create multiple notes at once (recommended: 10-20 notes per batch)",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "notes": {
                            "type": "array",
                            "maxItems": 50,
                            "items": {
                                "type": "object",
                                "properties": {
                                    "type": {"type": "string"},
                                    "deck": {"type": "string"},
                                    "fields": {"type": "object"},
                                    "tags": {"type": "array", "items": {"type": "string"}},
                                },
                                "required": ["type", "deck", "fields"],
                            },
                        },
                        "allowDuplicate": {"type": "boolean"},
                        "stopOnError": {"type": "boolean"},
                    },
                    "required": ["notes"],
                },
            ),
            Tool(
                name="search_notes",
                description="Search for notes using Anki query syntax",
                inputSchema={
                    "type": "object",
                    "properties": {"query": {"type": "string", "description": "Anki search query"}},
                    "required": ["query"],
                },
            ),
            Tool(
                name="get_note_info",
                description="Get detailed information about a note",
                inputSchema={
                    "type": "object",
                    "properties": {"noteId": {"type": "number", "description": "Note ID"}},
                    "required": ["noteId"],
                },
            ),
            Tool(
                name="update_note",
                description="Update an existing note",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "id": {"type": "number", "description": "Note ID"},
                        "fields": {"type": "object", "description": "Fields to update"},
                        "tags": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "New tags",
                        },
                    },
                    "required": ["id", "fields"],
                },
            ),
            Tool(
                name="delete_note",
                description="Delete a note",
                inputSchema={
                    "type": "object",
                    "properties": {"noteId": {"type": "number", "description": "Note ID"}},
                    "required": ["noteId"],
                },
            ),
        ]

    async def execute_tool(self, name: str, arguments: dict[str, Any]) -> list[TextContent]:
        """Execute a tool by name.

        Args:
            name: Tool name
            arguments: Tool arguments

        Returns:
            List of text content responses

        Raises:
            ValueError: If tool not found
            AnkiConnectError: If Anki operation fails
        """
        handlers = {
            "list_decks": self._list_decks,
            "create_deck": self._create_deck,
            "list_note_types": self._list_note_types,
            "get_note_type_info": self._get_note_type_info,
            "create_note_type": self._create_note_type,
            "create_note": self._create_note,
            "batch_create_notes": self._batch_create_notes,
            "search_notes": self._search_notes,
            "get_note_info": self._get_note_info,
            "update_note": self._update_note,
            "delete_note": self._delete_note,
        }

        handler = handlers.get(name)
        if not handler:
            raise ValueError(f"Unknown tool: {name}")

        return await handler(arguments)

    async def _list_decks(self, args: dict[str, Any]) -> list[TextContent]:
        decks = await self.client.get_deck_names()
        import json

        return [
            TextContent(
                type="text", text=json.dumps({"decks": decks, "count": len(decks)}, indent=2)
            )
        ]

    async def _create_deck(self, args: dict[str, Any]) -> list[TextContent]:
        if not args.get("name"):
            raise ValueError("Deck name is required")
        deck_id = await self.client.create_deck(args["name"])
        import json

        return [
            TextContent(
                type="text", text=json.dumps({"success": True, "deckId": deck_id}, indent=2)
            )
        ]

    async def _list_note_types(self, args: dict[str, Any]) -> list[TextContent]:
        note_types = await self.client.get_model_names()
        import json

        return [
            TextContent(
                type="text",
                text=json.dumps({"noteTypes": note_types, "count": len(note_types)}, indent=2),
            )
        ]

    async def _get_note_type_info(self, args: dict[str, Any]) -> list[TextContent]:
        model_name = args.get("modelName")
        if not model_name:
            raise ValueError("modelName is required")

        fields = await self.client.get_model_field_names(model_name)
        templates = await self.client.get_model_templates(model_name)

        result = {"modelName": model_name, "fields": fields, "templates": templates}

        if args.get("includeCss"):
            styling = await self.client.get_model_styling(model_name)
            result["css"] = styling.get("css", "")

        import json

        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    async def _create_note_type(self, args: dict[str, Any]) -> list[TextContent]:
        name = args.get("name")
        fields = args.get("fields")
        templates = args.get("templates")
        css = args.get("css", "")

        if not all([name, fields, templates]):
            raise ValueError("name, fields, and templates are required")

        card_templates = [
            {"Name": t["name"], "Front": t["front"], "Back": t["back"]} for t in templates
        ]

        result = await self.client.create_model(name, fields, css, card_templates)
        import json

        return [
            TextContent(type="text", text=json.dumps({"success": True, "model": result}, indent=2))
        ]

    async def _create_note(self, args: dict[str, Any]) -> list[TextContent]:
        note_type = args.get("type")
        deck = args.get("deck")
        fields = args.get("fields")
        tags = args.get("tags", [])
        allow_duplicate = args.get("allowDuplicate", False)

        if not all([note_type, deck, fields]):
            raise ValueError("type, deck, and fields are required")

        note = {
            "deckName": deck,
            "modelName": note_type,
            "fields": fields,
            "tags": tags,
            "options": {"allowDuplicate": allow_duplicate},
        }

        note_id = await self.client.add_note(note)
        import json

        return [
            TextContent(
                type="text", text=json.dumps({"success": True, "noteId": note_id}, indent=2)
            )
        ]

    async def _batch_create_notes(self, args: dict[str, Any]) -> list[TextContent]:
        notes_data = args.get("notes", [])
        allow_duplicate = args.get("allowDuplicate", False)
        stop_on_error = args.get("stopOnError", False)

        if len(notes_data) > 50:
            raise ValueError("Maximum 50 notes per batch")

        notes = []
        for note_data in notes_data:
            notes.append(
                {
                    "deckName": note_data["deck"],
                    "modelName": note_data["type"],
                    "fields": note_data["fields"],
                    "tags": note_data.get("tags", []),
                    "options": {"allowDuplicate": allow_duplicate},
                }
            )

        note_ids = await self.client.add_notes(notes)

        results = []
        for i, note_id in enumerate(note_ids):
            if note_id is None:
                results.append({"index": i, "success": False, "error": "Failed to create note"})
                if stop_on_error:
                    break
            else:
                results.append({"index": i, "success": True, "noteId": note_id})

        import json

        return [
            TextContent(
                type="text", text=json.dumps({"results": results, "total": len(results)}, indent=2)
            )
        ]

    async def _search_notes(self, args: dict[str, Any]) -> list[TextContent]:
        query = args.get("query")
        if not query:
            raise ValueError("query is required")

        note_ids = await self.client.find_notes(query)

        notes = []
        if note_ids:
            limit = min(len(note_ids), 50)
            notes_info = await self.client.notes_info(note_ids[:limit])
            notes = notes_info

        import json

        return [
            TextContent(
                type="text",
                text=json.dumps(
                    {
                        "query": query,
                        "total": len(note_ids),
                        "notes": notes,
                        "limitApplied": len(note_ids) > 50,
                    },
                    indent=2,
                ),
            )
        ]

    async def _get_note_info(self, args: dict[str, Any]) -> list[TextContent]:
        note_id = args.get("noteId")
        if not note_id:
            raise ValueError("noteId is required")

        notes_info = await self.client.notes_info([note_id])
        if not notes_info:
            raise ValueError(f"Note not found: {note_id}")

        import json

        return [TextContent(type="text", text=json.dumps(notes_info[0], indent=2))]

    async def _update_note(self, args: dict[str, Any]) -> list[TextContent]:
        note_id = args.get("id")
        fields = args.get("fields")
        tags = args.get("tags")

        if not note_id or not fields:
            raise ValueError("id and fields are required")

        await self.client.update_note_fields(note_id, fields)

        if tags is not None:
            await self.client.update_note_tags(note_id, tags)

        import json

        return [
            TextContent(
                type="text", text=json.dumps({"success": True, "noteId": note_id}, indent=2)
            )
        ]

    async def _delete_note(self, args: dict[str, Any]) -> list[TextContent]:
        note_id = args.get("noteId")
        if not note_id:
            raise ValueError("noteId is required")

        await self.client.delete_notes([note_id])
        import json

        return [
            TextContent(
                type="text", text=json.dumps({"success": True, "noteId": note_id}, indent=2)
            )
        ]
