# relationship-resolution Specification

## Purpose
TBD - created by archiving change add-django-model-scanner. Update Purpose after archive.
## Requirements
### Requirement: Relationship Field Identification

The system SHALL identify relationship fields by checking if the field type is one of ForeignKey, OneToOneField, or ManyToManyField, creating a separate relationship record in addition to the field definition.

#### Scenario: ForeignKey relationship

- **WHEN** a field is defined as `models.ForeignKey("Group", on_delete=models.CASCADE)`
- **THEN** it is identified as a relationship field of type ForeignKey

#### Scenario: OneToOneField relationship

- **WHEN** a field is defined as `models.OneToOneField("Profile", on_delete=models.CASCADE)`
- **THEN** it is identified as a OneToOne relationship

#### Scenario: ManyToManyField relationship

- **WHEN** a field is defined as `models.ManyToManyField("Tag")`
- **THEN** it is identified as a ManyToMany relationship

### Requirement: Target Model Resolution

The system SHALL resolve the target model from the first positional argument of relationship fields, handling both string references and direct class references.

#### Scenario: String reference to app model

- **WHEN** a ForeignKey uses `"auth.Group"` as target
- **THEN** the target is resolved to qualified name `auth.models.Group`

#### Scenario: String reference to same-app model

- **WHEN** a ForeignKey uses `"User"` without app prefix in the `accounts` app
- **THEN** the target is resolved to `accounts.models.User`

#### Scenario: Self-referential string

- **WHEN** a ForeignKey uses `"self"` as target
- **THEN** the target is set to the model's own qualified name

#### Scenario: Direct class reference

- **WHEN** a ForeignKey uses `from .models import Group; group = ForeignKey(Group, ...)`
- **THEN** the system extracts the class name and resolves to qualified name

### Requirement: Relationship Cascade Behavior

The system SHALL extract the `on_delete` option for ForeignKey and OneToOneField relationships, recording the cascade behavior for schema analysis.

#### Scenario: CASCADE on_delete

- **WHEN** a ForeignKey has `on_delete=models.CASCADE`
- **THEN** the relationship metadata includes `on_delete: "CASCADE"`

#### Scenario: PROTECT on_delete

- **WHEN** a ForeignKey has `on_delete=models.PROTECT`
- **THEN** the relationship metadata includes `on_delete: "PROTECT"`

#### Scenario: SET_NULL with nullable field

- **WHEN** a ForeignKey has `on_delete=models.SET_NULL, null=True`
- **THEN** both the cascade behavior and null constraint are recorded

### Requirement: Related Name Tracking

The system SHALL extract the `related_name` option from relationship fields to document reverse relationship accessors.

#### Scenario: Explicit related_name

- **WHEN** a ForeignKey has `related_name="members"`
- **THEN** the relationship metadata includes `related_name: "members"`

#### Scenario: Related_name with plus sign

- **WHEN** a ForeignKey has `related_name="+"`
- **THEN** it is recorded, indicating no reverse relation

#### Scenario: Default related_name

- **WHEN** no `related_name` is specified
- **THEN** the metadata omits the field or marks it as null (Django generates default)

### Requirement: Through Model for ManyToMany

The system SHALL extract the `through` option from ManyToManyField relationships, identifying explicit intermediate models for complex many-to-many relationships.

#### Scenario: Explicit through model

- **WHEN** a ManyToManyField has `through="Membership"`
- **THEN** the relationship metadata includes `through: "app.models.Membership"`

#### Scenario: Through model with full path

- **WHEN** a ManyToManyField has `through="accounts.Membership"`
- **THEN** the full path is preserved in metadata

#### Scenario: No through model

- **WHEN** no `through` option is specified
- **THEN** Django creates an implicit intermediary table (not tracked in this spec)

### Requirement: Relationship Symmetry for Self-References

The system SHALL handle `symmetrical` option for self-referential ManyToManyField relationships.

#### Scenario: Symmetrical self-reference

- **WHEN** a ManyToManyField uses `"self"` with `symmetrical=True` (default)
- **THEN** the relationship is marked as bidirectional

#### Scenario: Asymmetrical self-reference

- **WHEN** a ManyToManyField uses `"self"` with `symmetrical=False`
- **THEN** the relationship is marked as directional (e.g., followers/following)

### Requirement: Foreign Key to Primary Key Mapping

The system SHALL extract the `to_field` option if specified, documenting non-standard foreign key target fields.

#### Scenario: Foreign key to custom field

- **WHEN** a ForeignKey has `to_field="slug"`
- **THEN** the relationship metadata includes `to_field: "slug"`

#### Scenario: Default to primary key

- **WHEN** no `to_field` is specified
- **THEN** the relationship targets the primary key (default behavior, may omit from output)

