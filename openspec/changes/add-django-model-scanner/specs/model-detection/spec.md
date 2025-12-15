# Model Detection Specification

## ADDED Requirements

### Requirement: Django Model Class Identification

The system SHALL identify Django model classes by analyzing their inheritance hierarchy through astroid's inference engine, detecting any class that inherits from `django.db.models.base.Model` regardless of import style or aliasing.

#### Scenario: Direct inheritance from Model

- **WHEN** a class directly inherits from `django.db.models.Model`
- **THEN** the class is identified as a Django model

#### Scenario: Indirect inheritance through custom base

- **WHEN** a class inherits from a custom base class that itself inherits from `django.db.models.Model`
- **THEN** the class is identified as a Django model through ancestor traversal

#### Scenario: Aliased import detection

- **WHEN** a model inherits from an aliased import like `from django.db.models import Model as DjangoModel`
- **THEN** the class is correctly identified using astroid's qualified name resolution

#### Scenario: Cross-file base class

- **WHEN** a model inherits from a base class defined in another module
- **THEN** astroid resolves the base class definition and detects the Model ancestry

### Requirement: Abstract Model Classification

The system SHALL determine if a model is abstract by inspecting its inner `Meta` class for an `abstract = True` attribute, using AST node type checking to avoid executing code.

#### Scenario: Abstract model with Meta class

- **WHEN** a model contains `class Meta` with `abstract = True`
- **THEN** the model is marked as abstract

#### Scenario: Concrete model without Meta

- **WHEN** a model has no `Meta` class or `abstract` is not set
- **THEN** the model is marked as concrete (non-abstract)

#### Scenario: Abstract false explicit

- **WHEN** a model has `class Meta` with `abstract = False`
- **THEN** the model is marked as concrete

### Requirement: Module and Qualified Name Tracking

The system SHALL record each model's fully qualified name (module path + class name) and source module for unambiguous identification across the project.

#### Scenario: Standard app structure

- **WHEN** scanning a model in `myapp/models.py` with class name `User`
- **THEN** the qualified name is recorded as `myapp.models.User`

#### Scenario: Split models file

- **WHEN** scanning a model in `myapp/models/user.py` with class name `User`
- **THEN** the qualified name is recorded as `myapp.models.user.User`

### Requirement: Non-Model Class Exclusion

The system SHALL exclude classes that do not inherit from Django's Model, including helper classes, mixins without Model ancestry, and unrelated classes in the same files.

#### Scenario: Helper class in models file

- **WHEN** a class does not inherit from `django.db.models.Model` or its descendants
- **THEN** the class is not included in the output

#### Scenario: Mixin without Model base

- **WHEN** a mixin class exists without Model inheritance
- **THEN** the mixin is excluded unless used by a concrete model

### Requirement: Database Table Name Resolution

The system SHALL extract the database table name from the `Meta.db_table` attribute if specified, otherwise derive it from Django's default naming convention (app_label + lowercase model name).

#### Scenario: Explicit db_table in Meta

- **WHEN** a model's `Meta` class defines `db_table = "custom_users"`
- **THEN** the table name is recorded as `custom_users`

#### Scenario: Default table naming

- **WHEN** no `db_table` is specified for model `User` in app `accounts`
- **THEN** the table name is derived as `accounts_user`

#### Scenario: Abstract model has no table

- **WHEN** a model is abstract
- **THEN** no table name is recorded or it is explicitly marked as null
