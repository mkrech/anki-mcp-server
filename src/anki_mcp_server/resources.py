"""MCP resource handlers for Anki metadata."""

import json
import time
from typing import Any

from mcp.types import Resource, ResourceTemplate

from anki_mcp_server.client import AnkiClient


class ResourceHandler:
    """Handles all MCP resource operations for Anki.

    Provides cached access to Anki metadata like decks and note types.

    Args:
        client: AnkiConnect client instance
        cache_expiry: Cache TTL in seconds (default: 300 = 5 minutes)
    """

    def __init__(self, client: AnkiClient, cache_expiry: int = 300):
        self.client = client
        self.cache_expiry = cache_expiry
        self._cache: dict[str, tuple[Any, float]] = {}

    def _get_cached(self, key: str) -> Any | None:
        """Get cached value if not expired."""
        if key in self._cache:
            value, timestamp = self._cache[key]
            if time.time() - timestamp < self.cache_expiry:
                return value
            del self._cache[key]
        return None

    def _set_cached(self, key: str, value: Any) -> None:
        """Store value in cache with current timestamp."""
        self._cache[key] = (value, time.time())

    def get_resource_list(self) -> list[Resource]:
        """Return list of available static resources."""
        return [
            Resource(
                uri="anki://decks/all",
                name="All Decks",
                description="Complete list of available decks",
                mimeType="application/json",
            ),
        ]

    def get_resource_templates(self) -> list[ResourceTemplate]:
        """Return list of available resource templates."""
        return [
            ResourceTemplate(
                uriTemplate="anki://note-types/{modelName}",
                name="Note Type Schema",
                description="Detailed structure information for a specific note type",
                mimeType="application/json",
            ),
            ResourceTemplate(
                uriTemplate="anki://note-types/all",
                name="All Note Types",
                description="List of all available note types",
                mimeType="application/json",
            ),
            ResourceTemplate(
                uriTemplate="anki://note-types/all-with-schemas",
                name="All Note Types with Schemas",
                description="Detailed structure information for all note types",
                mimeType="application/json",
            ),
            ResourceTemplate(
                uriTemplate="anki://decks/all",
                name="All Decks",
                description="Complete list of available decks",
                mimeType="application/json",
            ),
        ]

    async def read_resource(self, uri: str) -> str:
        """Read a resource by URI.

        Args:
            uri: Resource URI

        Returns:
            JSON string with resource data

        Raises:
            ValueError: If URI is not supported
        """
        if uri == "anki://decks/all":
            return await self._read_decks()
        elif uri == "anki://note-types/all":
            return await self._read_note_types()
        elif uri == "anki://note-types/all-with-schemas":
            return await self._read_all_schemas()
        elif uri.startswith("anki://note-types/"):
            model_name = uri.replace("anki://note-types/", "")
            return await self._read_model_schema(model_name)
        else:
            raise ValueError(f"Unknown resource URI: {uri}")

    async def _read_decks(self) -> str:
        """Read all decks."""
        decks = await self.client.get_deck_names()
        return json.dumps({"decks": decks, "count": len(decks)}, indent=2)

    async def _read_note_types(self) -> str:
        """Read all note type names with caching."""
        cached = self._get_cached("note_types")
        if cached:
            return cached

        note_types = await self.client.get_model_names()
        result = json.dumps({"noteTypes": note_types, "count": len(note_types)}, indent=2)
        self._set_cached("note_types", result)
        return result

    async def _read_model_schema(self, model_name: str) -> str:
        """Read schema for a specific note type with caching."""
        cache_key = f"schema:{model_name}"
        cached = self._get_cached(cache_key)
        if cached:
            return cached

        fields = await self.client.get_model_field_names(model_name)
        templates = await self.client.get_model_templates(model_name)
        styling = await self.client.get_model_styling(model_name)

        schema = {
            "modelName": model_name,
            "fields": fields,
            "templates": templates,
            "css": styling.get("css", ""),
        }

        result = json.dumps(schema, indent=2)
        self._set_cached(cache_key, result)
        return result

    async def _read_all_schemas(self) -> str:
        """Read schemas for all note types with caching."""
        cached = self._get_cached("all_schemas")
        if cached:
            return cached

        note_types = await self.client.get_model_names()
        schemas = []

        for model_name in note_types:
            fields = await self.client.get_model_field_names(model_name)
            templates = await self.client.get_model_templates(model_name)
            styling = await self.client.get_model_styling(model_name)

            schemas.append(
                {
                    "modelName": model_name,
                    "fields": fields,
                    "templates": templates,
                    "css": styling.get("css", ""),
                }
            )

        result = json.dumps(schemas, indent=2)
        self._set_cached("all_schemas", result)
        return result

    def clear_cache(self) -> None:
        """Clear all cached data."""
        self._cache.clear()
