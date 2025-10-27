"""AnkiConnect client wrapper - Anti-corruption layer for Anki API."""

import os
from typing import Any

import httpx


class AnkiConnectError(Exception):
    """Exception raised when AnkiConnect API returns an error."""

    pass


class AnkiClient:
    """Client for communicating with AnkiConnect API.

    Provides a clean interface to Anki operations and handles connection
    management, error handling, and retries.

    Args:
        url: AnkiConnect URL (default: http://localhost:8765, or from ANKI_CONNECT_PORT env var)
        timeout: Request timeout in seconds (default: 30)
    """

    def __init__(self, url: str | None = None, timeout: float = 30.0):
        if url is None:
            port = os.environ.get("ANKI_CONNECT_PORT", "8765")
            url = f"http://localhost:{port}"
        self.url = url
        self.timeout = timeout
        self._client = httpx.AsyncClient(timeout=timeout)

    async def _invoke(self, action: str, **params: Any) -> Any:
        """Invoke AnkiConnect API action.

        Args:
            action: AnkiConnect action name
            **params: Action parameters

        Returns:
            Result from AnkiConnect

        Raises:
            AnkiConnectError: If request fails or returns error
        """
        payload = {"action": action, "version": 6}
        if params:
            payload["params"] = params

        try:
            response = await self._client.post(self.url, json=payload)
            response.raise_for_status()
            data = response.json()

            if data.get("error"):
                raise AnkiConnectError(data["error"])

            return data.get("result")
        except httpx.HTTPError as e:
            raise AnkiConnectError(f"Failed to connect to AnkiConnect: {e}")

    async def check_connection(self) -> None:
        """Verify Anki is running and AnkiConnect is available.

        Raises:
            AnkiConnectError: If connection fails
        """
        await self._invoke("version")

    async def get_deck_names(self) -> list[str]:
        """List all deck names.

        Returns:
            List of deck names
        """
        return await self._invoke("deckNames")

    async def create_deck(self, name: str) -> int:
        """Create a new deck.

        Args:
            name: Deck name (can include :: for nesting)

        Returns:
            Deck ID
        """
        return await self._invoke("createDeck", deck=name)

    async def get_model_names(self) -> list[str]:
        """List all note type (model) names.

        Returns:
            List of note type names
        """
        return await self._invoke("modelNames")

    async def get_model_field_names(self, model_name: str) -> list[str]:
        """Get field names for a note type.

        Args:
            model_name: Note type name

        Returns:
            List of field names
        """
        return await self._invoke("modelFieldNames", modelName=model_name)

    async def get_model_templates(self, model_name: str) -> dict[str, list[str]]:
        """Get templates for a note type.

        Args:
            model_name: Note type name

        Returns:
            Dictionary with template names and fronts/backs
        """
        return await self._invoke("modelTemplates", modelName=model_name)

    async def get_model_styling(self, model_name: str) -> dict[str, str]:
        """Get CSS styling for a note type.

        Args:
            model_name: Note type name

        Returns:
            Dictionary with 'css' key
        """
        return await self._invoke("modelStyling", modelName=model_name)

    async def create_model(
        self,
        model_name: str,
        in_order_fields: list[str],
        css: str,
        card_templates: list[dict[str, str]],
    ) -> dict[str, Any]:
        """Create a new note type.

        Args:
            model_name: Name for the new note type
            in_order_fields: List of field names
            css: CSS styling
            card_templates: List of template dicts with 'Name', 'Front', 'Back'

        Returns:
            Model information
        """
        return await self._invoke(
            "createModel",
            modelName=model_name,
            inOrderFields=in_order_fields,
            css=css,
            cardTemplates=card_templates,
        )

    async def add_note(self, note: dict[str, Any]) -> int:
        """Add a single note.

        Args:
            note: Note data with deckName, modelName, fields, tags

        Returns:
            Note ID
        """
        return await self._invoke("addNote", note=note)

    async def add_notes(self, notes: list[dict[str, Any]]) -> list[int | None]:
        """Add multiple notes.

        Args:
            notes: List of note data dictionaries

        Returns:
            List of note IDs (None for failed notes)
        """
        return await self._invoke("addNotes", notes=notes)

    async def find_notes(self, query: str) -> list[int]:
        """Search for notes using Anki query syntax.

        Args:
            query: Anki search query

        Returns:
            List of note IDs
        """
        return await self._invoke("findNotes", query=query)

    async def notes_info(self, note_ids: list[int]) -> list[dict[str, Any]]:
        """Get detailed information for notes.

        Args:
            note_ids: List of note IDs

        Returns:
            List of note information dictionaries
        """
        return await self._invoke("notesInfo", notes=note_ids)

    async def update_note_fields(self, note_id: int, fields: dict[str, str]) -> None:
        """Update note fields.

        Args:
            note_id: Note ID
            fields: Dictionary of field names to values
        """
        note = {"id": note_id, "fields": fields}
        await self._invoke("updateNoteFields", note=note)

    async def update_note_tags(self, note_id: int, tags: list[str]) -> None:
        """Update note tags.

        Args:
            note_id: Note ID
            tags: List of tags
        """
        await self._invoke("updateNoteTags", note=note_id, tags=" ".join(tags))

    async def delete_notes(self, note_ids: list[int]) -> None:
        """Delete notes.

        Args:
            note_ids: List of note IDs to delete
        """
        await self._invoke("deleteNotes", notes=note_ids)

    async def can_add_notes(self, notes: list[dict[str, Any]]) -> list[bool]:
        """Check if notes can be added (duplicate detection).

        Args:
            notes: List of note data dictionaries

        Returns:
            List of booleans indicating if each note can be added
        """
        return await self._invoke("canAddNotes", notes=notes)

    async def close(self) -> None:
        """Close the HTTP client."""
        await self._client.aclose()
