# Abstract Inheritance Specification

## ADDED Requirements

### Requirement: Abstract Base Model Field Collection

The system SHALL collect all fields defined in abstract models separately, maintaining them in memory for inheritance merging into concrete child models.

#### Scenario: Abstract model with common fields

- **WHEN** an abstract model defines `created_at` and `updated_at` timestamp fields
- **THEN** these fields are collected and marked as inheritable

#### Scenario: Abstract model with relationships

- **WHEN** an abstract model defines a ForeignKey or ManyToManyField
- **THEN** the relationship is collected for inheritance

### Requirement: Field Inheritance into Child Models

The system SHALL merge fields from abstract base models into child models that inherit from them, with child fields overriding parent fields of the same name.

#### Scenario: Single abstract parent

- **WHEN** a concrete model inherits from one abstract base with 3 fields
- **THEN** all 3 fields are included in the child model's field list

#### Scenario: Child overrides parent field

- **WHEN** a child model defines a field with the same name as an abstract parent field
- **THEN** the child's field definition takes precedence

#### Scenario: Multiple abstract parents

- **WHEN** a model inherits from two abstract bases with non-overlapping fields
- **THEN** fields from both parents are merged into the child

### Requirement: Meta Options Inheritance Handling

The system SHALL NOT inherit `abstract = True` from parent models; concrete child models must explicitly set `abstract = False` or omit it to be treated as concrete.

#### Scenario: Concrete child of abstract parent

- **WHEN** a model inherits from an abstract base but does not set `abstract = True`
- **THEN** it is treated as a concrete model with its own database table

#### Scenario: Abstract child of abstract parent

- **WHEN** a model inherits from an abstract base and sets `abstract = True`
- **THEN** it is also treated as abstract and its fields are available for further inheritance

### Requirement: Ancestor Traversal for Multi-Level Inheritance

The system SHALL traverse the entire inheritance hierarchy to collect fields from all abstract ancestors, handling multi-level abstract base chains.

#### Scenario: Three-level abstract inheritance

- **WHEN** `ConcreteModel` inherits from `AbstractMiddle` which inherits from `AbstractBase`
- **THEN** fields from both `AbstractMiddle` and `AbstractBase` are merged into `ConcreteModel`

#### Scenario: Diamond inheritance pattern

- **WHEN** a model inherits from two abstract classes that both inherit from a common abstract base
- **THEN** fields from the common base are included once (no duplication)

### Requirement: Field Order Preservation

The system SHALL preserve the order of inherited fields according to Python's Method Resolution Order (MRO), with parent fields appearing before child-defined fields.

#### Scenario: Parent then child field order

- **WHEN** an abstract parent defines `id` and `created_at`, and child defines `name`
- **THEN** the output order is `id`, `created_at`, `name`

#### Scenario: Multiple inheritance field order

- **WHEN** a model inherits from two abstract parents
- **THEN** fields are ordered according to the inheritance list (left to right in base class tuple)

### Requirement: Relationship Inheritance

The system SHALL inherit relationship fields (ForeignKey, ManyToManyField) from abstract parents, properly resolving relationship targets in the child model context.

#### Scenario: Inherited ForeignKey

- **WHEN** an abstract base has `created_by = ForeignKey("User", ...)`
- **THEN** all concrete children inherit this relationship

#### Scenario: Inherited ManyToManyField

- **WHEN** an abstract base has `tags = ManyToManyField("Tag")`
- **THEN** each concrete child gets its own many-to-many relationship to Tag

### Requirement: Abstract Model Output Inclusion

The system SHALL include abstract models in the YAML output with `abstract: true` metadata, allowing documentation of inheritance hierarchies even though they have no database tables.

#### Scenario: Abstract model in output

- **WHEN** scanning a codebase with abstract models
- **THEN** they appear in YAML with their fields and `abstract: true`

#### Scenario: Abstract model reference resolution

- **WHEN** a concrete model inherits from an abstract model
- **THEN** the inheritance relationship can be traced through the YAML structure
