# VS Code / Cline Integration

## Verwendung mit Cline (VS Code Extension)

### Installation

1. **Cline Extension installieren:**
   - Öffne VS Code
   - Gehe zu Extensions (Cmd+Shift+X)
   - Suche nach "Cline"
   - Installiere die Extension

2. **Anki vorbereiten:**
   - Starte Anki Desktop
   - Stelle sicher, dass AnkiConnect installiert ist
   - AnkiConnect läuft automatisch auf Port 8765

3. **MCP Server konfigurieren:**

   Öffne die Cline Settings in VS Code und füge folgende Konfiguration hinzu:

   ```json
   {
     "mcpServers": {
       "anki": {
         "command": "uv",
         "args": [
           "--directory",
           "/Users/michaelkrech/_work/anki-tutor",
           "run",
           "anki-mcp-server"
         ]
       }
     }
   }
   ```

   **Oder für systemweite Installation:**
   ```json
   {
     "mcpServers": {
       "anki": {
         "command": "uv",
         "args": ["run", "--with", "anki-mcp-server", "anki-mcp-server"]
       }
     }
   }
   ```

4. **Neustart:**
   - Restart Cline Extension
   - Der Anki MCP Server sollte jetzt verfügbar sein

### Verwendung

Öffne Cline Chat und teste:

```
"Liste alle meine Anki Decks auf"
```

```
"Erstelle eine neue Karte im Deck 'Deutsch':
Vorderseite: Was ist die Hauptstadt von Frankreich?
Rückseite: Paris"
```

```
"Erstelle 5 Vokabelkarten für Spanisch-Grundwortschatz"
```

```
"Wandle diesen Text in Lückentexte um:
Die Photosynthese ist der Prozess, bei dem Pflanzen 
Lichtenergie in chemische Energie umwandeln."
```

## Verwendung mit GitHub Copilot Chat

Wenn du GitHub Copilot Chat in VS Code verwendest:

1. Öffne die Settings (`~/.config/github-copilot/mcp-settings.json` oder über VS Code Settings)
2. Füge die gleiche Konfiguration hinzu wie oben

## Debugging

### Server Logs anzeigen

```bash
# In Terminal
uv run anki-mcp-server --log-level DEBUG
```

### Häufige Probleme

**"Failed to connect to Anki":**
- ✅ Anki läuft
- ✅ AnkiConnect installiert (Tools → Add-ons)
- ✅ Anki neu starten

**"Command not found: uv":**
```bash
# uv installieren
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Server startet nicht:**
```bash
# Dependencies installieren
cd /Users/michaelkrech/_work/anki-tutor
uv pip install -e ".[dev]"
```

## MCP Inspector (Debugging Tool)

Für detailliertes Debugging:

```bash
# MCP Inspector starten
npx @modelcontextprotocol/inspector uv --directory /Users/michaelkrech/_work/anki-tutor run anki-mcp-server
```

Dies öffnet eine Web-UI zum Testen aller Tools und Resources.

## Custom Port

Falls AnkiConnect auf einem anderen Port läuft:

```json
{
  "mcpServers": {
    "anki": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/michaelkrech/_work/anki-tutor",
        "run",
        "anki-mcp-server",
        "--port",
        "8080"
      ]
    }
  }
}
```
