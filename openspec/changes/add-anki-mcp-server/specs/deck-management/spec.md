## ADDED Requirements

### Requirement: List Decks
The system SHALL provide a tool to list all available Anki decks.

#### Scenario: List all decks successfully
- **WHEN** the `list_decks` tool is invoked
- **THEN** return a JSON response containing all deck names and total count

#### Scenario: Anki not running
- **WHEN** the `list_decks` tool is invoked and Anki is not running
- **THEN** return an MCP error with code `InternalError` and message indicating Anki is not available

### Requirement: Create Deck
The system SHALL provide a tool to create a new Anki deck with a specified name.

#### Scenario: Create deck successfully
- **WHEN** the `create_deck` tool is invoked with a valid deck name
- **THEN** create the deck in Anki and return success confirmation with deck ID

#### Scenario: Create deck with existing name
- **WHEN** the `create_deck` tool is invoked with a name that already exists
- **THEN** return success (idempotent operation, deck already exists)

#### Scenario: Create deck with invalid name
- **WHEN** the `create_deck` tool is invoked with an empty or null name
- **THEN** return an MCP error with code `InvalidParams` and descriptive message

#### Scenario: Create nested deck
- **WHEN** the `create_deck` tool is invoked with a name containing "::" separators
- **THEN** create nested deck structure following Anki conventions
