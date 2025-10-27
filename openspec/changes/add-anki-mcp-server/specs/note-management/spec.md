## ADDED Requirements

### Requirement: Create Single Note
The system SHALL provide a tool to create individual notes in Anki with support for Basic and Cloze note types.

#### Scenario: Create Basic note successfully
- **WHEN** the `create_note` tool is invoked with type "Basic", deck name, Front and Back fields
- **THEN** create the note in Anki and return the note ID

#### Scenario: Create Cloze note successfully
- **WHEN** the `create_note` tool is invoked with type "Cloze", deck name, and Text field containing cloze deletions
- **THEN** create the cloze note in Anki and return the note ID

#### Scenario: Create note with tags
- **WHEN** the `create_note` tool is invoked with optional tags array
- **THEN** create the note with specified tags attached

#### Scenario: Create note in non-existent deck
- **WHEN** the `create_note` tool is invoked with a deck name that doesn't exist
- **THEN** return an MCP error with code `InvalidParams` indicating deck not found

#### Scenario: Create note with missing required fields
- **WHEN** the `create_note` tool is invoked without required fields for the note type
- **THEN** return an MCP error with code `InvalidParams` listing missing fields

#### Scenario: Create duplicate note
- **WHEN** the `create_note` tool is invoked with `allowDuplicate: false` and matching content exists
- **THEN** return an MCP error indicating duplicate detected

#### Scenario: Allow duplicate note
- **WHEN** the `create_note` tool is invoked with `allowDuplicate: true`
- **THEN** create the note even if duplicate content exists

### Requirement: Batch Create Notes
The system SHALL provide a tool to create multiple notes efficiently in a single operation.

#### Scenario: Batch create multiple notes successfully
- **WHEN** the `batch_create_notes` tool is invoked with an array of 10 note specifications
- **THEN** create all notes and return an array of note IDs

#### Scenario: Batch create with mixed success
- **WHEN** the `batch_create_notes` tool is invoked with `stopOnError: false` and some notes are invalid
- **THEN** create all valid notes and return results with success/error status for each

#### Scenario: Batch create stops on error
- **WHEN** the `batch_create_notes` tool is invoked with `stopOnError: true` and an error occurs
- **THEN** stop processing remaining notes and return error with partial results

#### Scenario: Batch create exceeds maximum size
- **WHEN** the `batch_create_notes` tool is invoked with more than 50 notes
- **THEN** return an MCP error indicating batch size limit exceeded

#### Scenario: Batch create with recommended size
- **WHEN** the `batch_create_notes` tool is invoked with 10-20 notes
- **THEN** process efficiently with optimal performance

### Requirement: Search Notes
The system SHALL provide a tool to search notes using Anki's query syntax.

#### Scenario: Search notes by query
- **WHEN** the `search_notes` tool is invoked with a valid Anki query string
- **THEN** return matching note IDs and detailed information for up to 50 notes

#### Scenario: Search with no results
- **WHEN** the `search_notes` tool is invoked with a query matching no notes
- **THEN** return empty results array with zero count

#### Scenario: Search with large result set
- **WHEN** the `search_notes` tool is invoked with a query matching more than 50 notes
- **THEN** return first 50 notes with indicator that limit was applied

#### Scenario: Search with invalid query syntax
- **WHEN** the `search_notes` tool is invoked with malformed query syntax
- **THEN** return an MCP error with code `InvalidParams` and query syntax help

### Requirement: Get Note Information
The system SHALL provide a tool to retrieve detailed information about a specific note.

#### Scenario: Get note info successfully
- **WHEN** the `get_note_info` tool is invoked with a valid note ID
- **THEN** return complete note details including fields, tags, note type, and card IDs

#### Scenario: Get note info for non-existent note
- **WHEN** the `get_note_info` tool is invoked with an invalid note ID
- **THEN** return an MCP error with code `InvalidParams` indicating note not found

### Requirement: Update Note
The system SHALL provide a tool to modify existing note fields and tags.

#### Scenario: Update note fields successfully
- **WHEN** the `update_note` tool is invoked with note ID and field updates
- **THEN** update the specified fields in Anki and return success confirmation

#### Scenario: Update note tags
- **WHEN** the `update_note` tool is invoked with note ID and new tags array
- **THEN** replace all tags with the new tags and return success

#### Scenario: Update note with partial fields
- **WHEN** the `update_note` tool is invoked with only some fields specified
- **THEN** update only the specified fields, leaving others unchanged

#### Scenario: Update non-existent note
- **WHEN** the `update_note` tool is invoked with an invalid note ID
- **THEN** return an MCP error with code `InvalidParams` indicating note not found

#### Scenario: Update note with invalid fields
- **WHEN** the `update_note` tool is invoked with fields not present in the note type
- **THEN** return an MCP error with code `InvalidParams` listing valid fields

### Requirement: Delete Note
The system SHALL provide a tool to permanently remove notes from Anki.

#### Scenario: Delete note successfully
- **WHEN** the `delete_note` tool is invoked with a valid note ID
- **THEN** delete the note and all associated cards from Anki and return success

#### Scenario: Delete non-existent note
- **WHEN** the `delete_note` tool is invoked with an invalid note ID
- **THEN** return an MCP error with code `InvalidParams` indicating note not found

#### Scenario: Delete note without ID
- **WHEN** the `delete_note` tool is invoked without a note ID parameter
- **THEN** return an MCP error with code `InvalidParams` requiring note ID
