## ADDED Requirements

### Requirement: Model Inheritance Base Classes Export

The system SHALL export a `bases` field in the model metadata section containing a list of direct Django Model base class fully qualified names, excluding `django.db.models.Model` itself.

#### Scenario: Concrete model with abstract parent

- **WHEN** a model `Post(TimestampedModel)` inherits from abstract base `TimestampedModel(models.Model)`
- **THEN** YAML output includes:
  ```yaml
  blog.models.Post:
    module: blog.models
    abstract: false
    bases:
      - blog.models.TimestampedModel
    fields: ...
  ```

#### Scenario: Model with multiple inheritance

- **WHEN** a model inherits from multiple base classes `Article(TimestampedModel, PublishableMixin)`
- **THEN** YAML output includes both bases in order:
  ```yaml
  bases:
    - blog.models.TimestampedModel
    - blog.models.PublishableMixin
  ```

#### Scenario: Direct Model inheritance

- **WHEN** a model inherits directly from `models.Model` with no intermediate classes
- **THEN** YAML output includes:
  ```yaml
  bases: []
  ```
  (empty list since `django.db.models.Model` is excluded)

#### Scenario: Abstract model inheritance chain

- **WHEN** an abstract model `TimestampedModel(models.Model)` is exported
- **THEN** its `bases` field is an empty list (only shows direct custom bases, not Django's Model)

## MODIFIED Requirements

### Requirement: Model Metadata Section

The system SHALL include model-level metadata including module path, abstract flag, inheritance bases, and database table name (for concrete models only).

#### Scenario: Concrete model metadata

- **WHEN** exporting a concrete model
- **THEN** metadata includes `module`, `abstract: false`, `bases` list, and `table` name

#### Scenario: Abstract model metadata

- **WHEN** exporting an abstract model
- **THEN** metadata includes `module`, `abstract: true`, `bases` list, and no `table` field

#### Scenario: Model with custom base classes

- **WHEN** exporting a model that inherits from custom Django model classes
- **THEN** metadata includes a `bases` field listing all direct parent Django models (excluding `django.db.models.Model`)
