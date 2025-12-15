# YAML Export Specification

## ADDED Requirements

### Requirement: YAML Structure Definition

The system SHALL export models as a YAML document with top-level keys being fully qualified model names, each containing metadata, fields, and relationships sections.

#### Scenario: Basic model export

- **WHEN** exporting a model `app.models.User`
- **THEN** the YAML has a top-level key `app.models.User` with nested structure

#### Scenario: Multiple models export

- **WHEN** exporting multiple models
- **THEN** each model is a separate top-level key in the YAML document

### Requirement: Model Metadata Section

The system SHALL include model-level metadata including module path, abstract flag, and database table name (for concrete models only).

#### Scenario: Concrete model metadata

- **WHEN** exporting a concrete model
- **THEN** metadata includes `module`, `abstract: false`, and `table` name

#### Scenario: Abstract model metadata

- **WHEN** exporting an abstract model
- **THEN** metadata includes `module`, `abstract: true`, and no `table` field

### Requirement: Fields Section Structure

The system SHALL export each field as a nested mapping under the `fields` key, with field name as key and field properties as value.

#### Scenario: Field with type and options

- **WHEN** a field is `name = CharField(max_length=100, null=False)`
- **THEN** YAML output is:
  ```yaml
  fields:
    name:
      type: CharField
      max_length: 100
      null: false
  ```

#### Scenario: Primary key field

- **WHEN** a field has `primary_key=True`
- **THEN** YAML includes `primary_key: true` in the field properties

### Requirement: Relationships Section Structure

The system SHALL export relationship fields separately under a `relationships` key, including target model and relationship-specific options.

#### Scenario: ForeignKey relationship export

- **WHEN** exporting a ForeignKey field
- **THEN** the relationships section includes:
  ```yaml
  relationships:
    group:
      type: ForeignKey
      to: app.models.Group
      on_delete: CASCADE
  ```

#### Scenario: ManyToManyField relationship export

- **WHEN** exporting a ManyToManyField
- **THEN** the relationships section includes type and target model

### Requirement: Boolean Value Normalization

The system SHALL normalize boolean string representations from AST (`"True"`, `"False"`) to proper YAML boolean values (`true`, `false`).

#### Scenario: Boolean field options

- **WHEN** a field has `null=True, blank=False`
- **THEN** YAML outputs `null: true` and `blank: false` (lowercase)

#### Scenario: Abstract flag normalization

- **WHEN** a model has `abstract = True` in Meta
- **THEN** YAML outputs `abstract: true`

### Requirement: Numeric Value Conversion

The system SHALL convert numeric string values from AST to proper YAML numeric types where possible.

#### Scenario: Max length as number

- **WHEN** a CharField has `max_length=100`
- **THEN** YAML outputs `max_length: 100` (not as string `"100"`)

#### Scenario: Decimal places

- **WHEN** a DecimalField has `max_digits=10, decimal_places=2`
- **THEN** both are output as numbers

### Requirement: String Value Preservation

The system SHALL preserve string values including choices, defaults, and help_text as quoted strings in YAML.

#### Scenario: Default string value

- **WHEN** a field has `default="active"`
- **THEN** YAML outputs `default: "active"`

#### Scenario: Help text with special characters

- **WHEN** a field has `help_text="User's email address"`
- **THEN** YAML properly escapes and quotes the string

### Requirement: Null and None Handling

The system SHALL represent Python `None` values as YAML `null` and distinguish between missing values and explicit `null`.

#### Scenario: Null default value

- **WHEN** a field has `default=None`
- **THEN** YAML outputs `default: null`

#### Scenario: Missing optional argument

- **WHEN** a field does not specify an optional argument like `related_name`
- **THEN** the key is omitted from YAML (not set to null)

### Requirement: Field Order Consistency

The system SHALL output fields in the order they appear in the model definition, preserving source code order for readability.

#### Scenario: Field definition order

- **WHEN** a model defines fields in order: id, name, email, created_at
- **THEN** YAML outputs them in the same order

### Requirement: Readable YAML Formatting

The system SHALL format YAML output with consistent indentation (2 spaces), no sorting of keys (preserve definition order), and clear visual structure.

#### Scenario: Two-space indentation

- **WHEN** generating YAML
- **THEN** nested levels use 2-space indentation

#### Scenario: No alphabetic sorting

- **WHEN** generating YAML with `yaml.safe_dump`
- **THEN** `sort_keys=False` is used to preserve insertion order

### Requirement: File Output Location

The system SHALL write the YAML output to a configurable file path, defaulting to `django_models.yaml` in the current working directory.

#### Scenario: Default output file

- **WHEN** no output path is specified
- **THEN** YAML is written to `./django_models.yaml`

#### Scenario: Custom output path

- **WHEN** a custom output path is provided via configuration
- **THEN** YAML is written to the specified path

### Requirement: Empty Project Handling

The system SHALL generate valid empty YAML `{}` when no Django models are found in the scanned project.

#### Scenario: No models found

- **WHEN** scanning a project with no Django models
- **THEN** output is valid YAML: `{}` or empty document
