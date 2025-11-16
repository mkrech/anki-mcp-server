## ADDED Requirements

### Requirement: Deck List Resource
The system SHALL provide an MCP resource exposing all available Anki decks.

#### Scenario: Read all decks resource
- **WHEN** the resource `anki://decks/all` is read
- **THEN** return JSON containing array of deck names and count

#### Scenario: Decks resource reflects current state
- **WHEN** a new deck is created in Anki
- **THEN** subsequent reads of `anki://decks/all` include the new deck

### Requirement: Note Types List Resource
The system SHALL provide an MCP resource exposing all available note types.

#### Scenario: Read all note types resource
- **WHEN** the resource `anki://note-types/all` is read
- **THEN** return JSON containing array of note type names and count

#### Scenario: Note types resource reflects additions
- **WHEN** a new note type is created
- **THEN** subsequent reads of `anki://note-types/all` include the new type

### Requirement: Note Types with Schemas Resource
The system SHALL provide an MCP resource exposing complete schemas for all note types.

#### Scenario: Read all schemas resource
- **WHEN** the resource `anki://note-types/all-with-schemas` is read
- **THEN** return JSON array with full schema for each note type including fields, templates, and CSS

#### Scenario: Schemas resource uses cache
- **WHEN** the resource `anki://note-types/all-with-schemas` is read multiple times within 5 minutes
- **THEN** return cached data without querying AnkiConnect

#### Scenario: Schemas resource cache expires
- **WHEN** the resource `anki://note-types/all-with-schemas` is read after 5-minute cache expiry
- **THEN** refresh data from AnkiConnect and update cache

### Requirement: Specific Note Type Schema Resource
The system SHALL provide an MCP resource template for retrieving individual note type schemas.

#### Scenario: Read specific note type schema
- **WHEN** the resource `anki://note-types/{modelName}` is read with a valid model name
- **THEN** return JSON with complete schema including fields, templates, and CSS

#### Scenario: Read schema for Basic note type
- **WHEN** the resource `anki://note-types/Basic` is read
- **THEN** return schema showing Front and Back fields with card template

#### Scenario: Read schema for Cloze note type
- **WHEN** the resource `anki://note-types/Cloze` is read
- **THEN** return schema showing Text and Extra fields with cloze template

#### Scenario: Read schema for non-existent type
- **WHEN** the resource `anki://note-types/{modelName}` is read with invalid model name
- **THEN** return an MCP error with code `InvalidParams` indicating model not found

#### Scenario: Schema cache per model
- **WHEN** specific note type schemas are read
- **THEN** cache each schema independently with 5-minute TTL

### Requirement: Resource List Discovery
The system SHALL provide resource list and template list endpoints for MCP clients.

#### Scenario: List available resources
- **WHEN** MCP client requests resource list
- **THEN** return all static resource URIs (decks, note types)

#### Scenario: List resource templates
- **WHEN** MCP client requests resource template list
- **THEN** return URI templates with parameter descriptions

### Requirement: Resource Cache Management
The system SHALL implement efficient caching for resource data.

#### Scenario: Cache expiry at 5 minutes
- **WHEN** cached resource data is older than 5 minutes
- **THEN** refresh from AnkiConnect on next access

#### Scenario: Cache per resource type
- **WHEN** multiple resources are accessed
- **THEN** maintain separate cache entries with independent expiry

#### Scenario: Cache clear on connection loss
- **WHEN** connection to Anki is lost and restored
- **THEN** optionally clear cache to ensure fresh data (implementation detail)
