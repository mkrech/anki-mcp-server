## ADDED Requirements

### Requirement: List Note Types
The system SHALL provide a tool to list all available note types (models) in Anki.

#### Scenario: List note types successfully
- **WHEN** the `list_note_types` tool is invoked
- **THEN** return an array of all note type names and total count

#### Scenario: List note types when Anki has only defaults
- **WHEN** the `list_note_types` tool is invoked on fresh Anki installation
- **THEN** return at minimum "Basic" and "Cloze" note types

### Requirement: Get Note Type Information
The system SHALL provide a tool to retrieve detailed structure information for a specific note type.

#### Scenario: Get note type structure successfully
- **WHEN** the `get_note_type_info` tool is invoked with a valid note type name
- **THEN** return complete structure including field names, templates, and CSS

#### Scenario: Get note type with includeCss option
- **WHEN** the `get_note_type_info` tool is invoked with `includeCss: true`
- **THEN** return structure including full CSS styling information

#### Scenario: Get note type without CSS
- **WHEN** the `get_note_type_info` tool is invoked with `includeCss: false` or omitted
- **THEN** return structure excluding CSS styling information

#### Scenario: Get non-existent note type
- **WHEN** the `get_note_type_info` tool is invoked with an invalid note type name
- **THEN** return an MCP error with code `InvalidParams` indicating note type not found

#### Scenario: Get Basic note type info
- **WHEN** the `get_note_type_info` tool is invoked with "Basic"
- **THEN** return structure showing "Front" and "Back" fields with corresponding templates

#### Scenario: Get Cloze note type info
- **WHEN** the `get_note_type_info` tool is invoked with "Cloze"
- **THEN** return structure showing "Text" and "Extra" fields with cloze template

### Requirement: Create Note Type
The system SHALL provide a tool to create custom note types with specified fields and templates.

#### Scenario: Create custom note type successfully
- **WHEN** the `create_note_type` tool is invoked with name, fields array, and templates array
- **THEN** create the note type in Anki and return success confirmation

#### Scenario: Create note type with CSS
- **WHEN** the `create_note_type` tool is invoked with optional CSS parameter
- **THEN** create the note type with specified styling

#### Scenario: Create note type with multiple templates
- **WHEN** the `create_note_type` tool is invoked with multiple card templates
- **THEN** create note type supporting multiple card types per note

#### Scenario: Create note type with existing name
- **WHEN** the `create_note_type` tool is invoked with a name that already exists
- **THEN** return an MCP error with code `InvalidParams` indicating name conflict

#### Scenario: Create note type without required fields
- **WHEN** the `create_note_type` tool is invoked without name, fields, or templates
- **THEN** return an MCP error with code `InvalidParams` listing required parameters

#### Scenario: Create note type with invalid template
- **WHEN** the `create_note_type` tool is invoked with templates missing required properties
- **THEN** return an MCP error with code `InvalidParams` specifying template requirements

### Requirement: Note Type Schema Validation
The system SHALL validate note type schemas before creating notes.

#### Scenario: Validate fields before note creation
- **WHEN** creating a note of a custom type
- **THEN** verify all required fields for that note type are provided

#### Scenario: Provide field guidance
- **WHEN** note creation fails due to missing fields
- **THEN** include available field names in error message for user guidance
