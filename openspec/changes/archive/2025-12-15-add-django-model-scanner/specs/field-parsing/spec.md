# Field Parsing Specification

## ADDED Requirements

### Requirement: Django Field Type Detection

The system SHALL identify Django field instances by analyzing assignment statements where the value is a call to a class that inherits from `django.db.models.fields.Field`, using astroid's inference to handle various import patterns.

#### Scenario: Standard field import

- **WHEN** a field is defined as `name = models.CharField(max_length=100)`
- **THEN** the system identifies it as a CharField

#### Scenario: Direct field import

- **WHEN** a field is defined as `from django.db.models import CharField; name = CharField(max_length=100)`
- **THEN** the system correctly identifies the CharField type

#### Scenario: Aliased field import

- **WHEN** a field is defined as `from django.db.models import CharField as Char; name = Char(max_length=100)`
- **THEN** the system resolves the alias and identifies it as CharField

#### Scenario: Custom field subclass

- **WHEN** a custom field class inherits from Field and is used in a model
- **THEN** the system identifies it through ancestor checking

### Requirement: Field Name Extraction

The system SHALL extract the field name from the left side of the assignment statement, handling both simple assignments and multiple target scenarios.

#### Scenario: Simple field assignment

- **WHEN** a field is defined as `email = models.EmailField()`
- **THEN** the field name is extracted as `email`

#### Scenario: Type-annotated assignment

- **WHEN** a field is defined as `email: str = models.EmailField()`
- **THEN** the field name is still extracted as `email` (annotation is ignored)

### Requirement: Field Options Parsing

The system SHALL extract all keyword arguments passed to field constructors, preserving option names and values as strings for later interpretation.

#### Scenario: Common field options

- **WHEN** a field is defined as `name = models.CharField(max_length=100, null=False, blank=True, default="")`
- **THEN** all options are extracted: `{"max_length": "100", "null": "False", "blank": "True", "default": '""'}`

#### Scenario: Complex option values

- **WHEN** a field has options like `choices=[(1, "Active"), (2, "Inactive")]`
- **THEN** the full expression is captured as a string representation

#### Scenario: Callable defaults

- **WHEN** a field has `default=timezone.now`
- **THEN** the default value is captured as the qualified name string `"timezone.now"`

### Requirement: Positional Argument Extraction

The system SHALL extract positional arguments from field constructors, which are critical for relationship fields (ForeignKey, ManyToManyField) to determine target models.

#### Scenario: ForeignKey with positional target

- **WHEN** a field is defined as `group = models.ForeignKey("auth.Group", on_delete=models.CASCADE)`
- **THEN** positional args include `['"auth.Group"']`

#### Scenario: ManyToMany with through model

- **WHEN** a field is defined as `tags = models.ManyToManyField("Tag", through="ArticleTag")`
- **THEN** positional args include `['"Tag"']` and options include `through`

### Requirement: Primary Key Detection

The system SHALL identify primary key fields by checking for `primary_key=True` option or recognizing AutoField, BigAutoField as implicit primary keys.

#### Scenario: Explicit primary key

- **WHEN** a field has `primary_key=True`
- **THEN** the field is marked as the primary key

#### Scenario: AutoField default primary key

- **WHEN** no explicit primary key exists and an AutoField named `id` is present
- **THEN** it is identified as the implicit primary key

#### Scenario: Custom primary key field

- **WHEN** a model uses `uuid = models.UUIDField(primary_key=True, default=uuid4)`
- **THEN** the system marks `uuid` as the primary key

### Requirement: Field Constraint Metadata

The system SHALL extract constraint-related options such as `null`, `blank`, `unique`, `db_index`, and validation constraints for documentation and validation purposes.

#### Scenario: Nullability and blank constraints

- **WHEN** a field has `null=True, blank=False`
- **THEN** both constraints are recorded in field metadata

#### Scenario: Uniqueness constraint

- **WHEN** a field has `unique=True`
- **THEN** the unique constraint is recorded

#### Scenario: Database index

- **WHEN** a field has `db_index=True`
- **THEN** the index metadata is captured

### Requirement: Non-Field Attribute Exclusion

The system SHALL exclude class attributes that are not Django fields, including properties, methods, class variables, and manager instances.

#### Scenario: Manager attribute

- **WHEN** a model has `objects = models.Manager()`
- **THEN** it is excluded from field parsing (managers are not fields)

#### Scenario: Property decorator

- **WHEN** a model has `@property` decorated methods
- **THEN** they are excluded from field output

#### Scenario: Class variable

- **WHEN** a model has a plain class variable like `VERBOSE_NAME = "User"`
- **THEN** it is not treated as a field
