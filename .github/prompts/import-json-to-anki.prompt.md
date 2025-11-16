---
description: Import flashcards from JSON files into Anki decks with page filtering
---

$ARGUMENTS
<!-- IMPORT-JSON-TO-ANKI:START -->
**Language**: Always communicate in German (Deutsch) with the user.

**Guardrails**
- Ensure Anki Desktop is running with AnkiConnect addon installed before starting
- Validate JSON file structure (must contain `sections` array)
- Create deck if it doesn't exist
- **Maximum 5 pages per import** - Prevents overwhelming generation and ensures quality
- Support batch imports (recommended: 10-20 cards per batch)
- Handle errors gracefully with clear error messages
- Show progress during import (e.g., "Importing cards 1-20 of 150...")
- If user requests more than 5 pages, suggest breaking into multiple imports

**Required JSON Structure**

The JSON file must contain a `sections` array from parsed PDF slides:

```json
{
  "file_path": "path/to/source.pdf",
  "metadata": {
    "parser": "docling",
    "filename": "02_tud_PGM02_BN1.pdf",
    "source_type": "slides",
    "document_kind": "slides",
    "lecture_nr": 2,
    "topic": "BN1"
  },
  "sections": [
    {
      "id": "section_id",
      "title": "Section Title",
      "content": "Section content with key concepts, definitions, formulas...",
      "level": 1,
      "page": 5,
      "parent_id": null,
      "image_path": "data/intermediate/slide_images/filename/slide_5.png"
    }
  ],
  "stats": {
    "total_sections": 78,
    "total_chars": 11964
  }
}
```

**The AI will automatically generate flashcards from these sections.**

**Steps**

1. **Load Sections JSON** - Parse the sections from the JSON file
2. **Analyze Sections** - Use AI to analyze content and determine optimal flashcards
3. **Generate Flashcards** - AI creates question-answer pairs with appropriate card types
4. **Check Anki Connection** - Verify Anki Desktop is running with AnkiConnect
5. **List Available Decks** - Show existing Anki decks or option to create new deck
6. **Select or Create Deck** - Choose existing deck or specify new deck name (e.g., "PGM::02_Bn1")
7. **Optional: Set Page Range** - Specify which pages to process (e.g., "pages 1-10" or "page 5" or leave empty for all)
8. **Optional: Set Card Type Distribution** - Specify preferred card type mix (see Card Type Distribution section below)
9. **Review Generated Cards** - Show sample of generated cards for approval
10. **Confirm Import** - Review the import plan (number of cards, deck name, page range, card types)
11. **Execute Import** - Use batch import to create cards in Anki
12. **Verify Import** - Check that cards were created successfully in Anki

**Page Filtering**
- **Default: First 5 pages only** - Always limit to max 5 pages unless user specifies fewer
- **Single page**: "page 5" or "p5"
- **Page range (max 5)**: "pages 1-5" or "p1-5" 
- **Multiple ranges (max 5 total)**: "pages 1-3, 8-9" or "p1-3,8-9" (5 pages total)
- **More than 5 pages requested**: Suggest splitting into multiple imports
  - Example: "Seiten 1-10" → "Zu viele Seiten! Bitte maximal 5 Seiten pro Import. Mach zuerst 1-5, dann 6-10."

**Card Type Distribution**

Users can specify their preferred card type mix when generating flashcards. The AI will attempt to match this distribution:

**Default Distribution (if not specified):**
- **Cloze: 55%** (Majority) - Fill-in-the-blank for definitions, formulas, key concepts
- **All-in-One (KPRIM/MC/SC): 45%** - Multiple choice, single choice, K-Prim statements
  - KPRIM: 30% - 4 statements with T/F evaluation (ideal for comparisons, properties)
  - MC: 10% - Multiple correct answers (concepts with several valid aspects)
  - SC: 5% - Single correct answer (clear-cut questions)
- **Basic: 0%** (NEVER USE) - Basic cards are NOT allowed

**User Preferences Examples:**
- **"Mehrheit Cloze, viel KPRIM"** 
  - Cloze: 55%, KPRIM: 35%, MC: 7%, SC: 3%, Basic: 0%
- **"Nur KPRIM und Cloze"**
  - KPRIM: 50%, Cloze: 50%, Basic: 0%, MC: 0%, SC: 0%
- **"Balanced Mix"**
  - Cloze: 40%, KPRIM: 30%, MC: 20%, SC: 10%, Basic: 0%

**How to Specify:**
During the workflow, when asked, the user can say:
- **"Standard Verteilung"** or **"Default"** → Uses default distribution (NO Basic!)
- **"Mehrheit Cloze und KPRIM"** → AI interprets as Cloze 50%, KPRIM 40%, MC 7%, SC 3%
- **"Nur Cloze"** → 100% Cloze cards
- **Custom percentages** → "50% Cloze, 30% KPRIM, 20% MC"

**AI Generation Strategy:**
1. Analyze section content for suitability to each card type
2. Generate cards attempting to match user's preferred distribution
3. Adapt if content doesn't fit (e.g., can't force KPRIM if no 4-way comparisons exist)
4. Show actual distribution in import plan for user review

**Note Types & Card Types**

The system supports these card types with automatic note type mapping:

| Card Type | Anki Note Type | Fields | Description |
|-----------|----------------|--------|-------------|
| `cloze` | Cloze | Text, Extra | Fill-in-the-blank cards with {{c1::deletions}} |
| `kprim` | AllInOne (kprim, mc, sc) | Question, Answer, Q_1-Q_5, Extra, Sources | K-Prim cards with 4 statements (each True/False) |
| `mc` | AllInOne (kprim, mc, sc) | Question, Answer, Q_1-Q_5, Extra, Sources | Multiple choice (multiple correct answers) |
| `sc` | AllInOne (kprim, mc, sc) | Question, Answer, Q_1-Q_5, Extra, Sources | Single choice (one correct answer) |

**⚠️ WICHTIG: Basic Cards sind NICHT erlaubt!**
- Verwende IMMER Cloze, KPRIM, MC oder SC
- Konvertiere einfache Fragen zu Cloze-Format
- Beispiel: "Was ist X?" → "X ist {{c1::...}}"

**WICHTIG: Note Type Name**
- Der korrekte Note Type Name in Anki ist: **"AllInOne (kprim, mc, sc)"** (NICHT "All-in-One")
- Beim Import MUSS dieser exakte Name verwendet werden

**AllInOne Note Type Structure:**
- **Question**: Main question text
- **Answer**: Correct answer(s) or solution explanation
- **Q_1 to Q_5**: Answer options or statements
- **Extra**: Additional context or explanations
- **Sources**: Source reference (e.g., "Folie 5", "Homework-1 Task 3")

**Note Type Requirements:**
- Ensure the note types exist in Anki before importing
- Use `mcp_anki_list_note_types` to check available note types
- The correct name is "AllInOne (kprim, mc, sc)" not "All-in-One"
- If missing, create them manually or the import will fail

**MCP Tools Used:**
- `mcp_anki_list_decks` - List available decks
- `mcp_anki_create_deck` - Create new deck if needed
- `mcp_anki_list_note_types` - Verify note types exist
- `mcp_anki_create_note` - Create single note
- `mcp_anki_batch_create_notes` - Batch import (recommended: 10-20 cards)

**Example Workflow**

See the detailed workflow examples in the original prompt for step-by-step interactions.

**Troubleshooting**
- **Anki not running**: Start Anki Desktop and ensure AnkiConnect addon is installed
- **JSON file not found**: Check the file path is correct relative to workspace root
- **Invalid JSON structure**: Ensure the file has a "sections" array with required fields
- **Deck already exists**: Cards will be added to existing deck (duplicates are checked by Anki)
- **Import errors**: Check Anki's error log and ensure note types exist
- **Wrong note type name**: Use "AllInOne (kprim, mc, sc)" not "All-in-One"
- **Check available note types**: Use `mcp_anki_list_note_types` tool first

<!-- IMPORT-JSON-TO-ANKI:END -->
