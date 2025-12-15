## ADDED Requirements

### Requirement: Literal Value Inference for Field Options

The system SHALL use astroid's inference capabilities to resolve field option values that are Python literals (lists, tuples, dicts, sets) and convert them from AST string representations to proper Python data structures for YAML export.

#### Scenario: Choices tuple inference

- **WHEN** a field is defined as `status = models.CharField(max_length=10, choices=[("active", "Active"), ("inactive", "Inactive")])`
- **THEN** the field options include:
  ```python
  {
    "type": "CharField",
    "max_length": 10,
    "choices": [["active", "Active"], ["inactive", "Inactive"]]
  }
  ```

#### Scenario: Integer choices inference

- **WHEN** a field has `choices=[(1, "Draft"), (2, "Published"), (3, "Archived")]`
- **THEN** the choices are exported as a proper list structure with integer keys

#### Scenario: Complex choices with groups

- **WHEN** a field has grouped choices `choices=[("Group1", [("a", "A"), ("b", "B")]), ("Group2", [("c", "C")])]`
- **THEN** the nested structure is properly inferred and exported

#### Scenario: Fallback for complex expressions

- **WHEN** choices reference a module-level constant like `choices=STATUS_CHOICES`
- **THEN** the system attempts inference but falls back to string representation if unable to resolve

### Requirement: List and Tuple Field Option Handling

The system SHALL properly handle field options that are defined as Python lists or tuples, such as `validators`, `unique_together`, and custom options.

#### Scenario: Validators list

- **WHEN** a field has `validators=[MinLengthValidator(5), MaxLengthValidator(100)]`
- **THEN** the system captures the list structure (may be string representation for complex validators)

#### Scenario: Default list value

- **WHEN** a field has `default=[]` or `default=[1, 2, 3]`
- **THEN** the default is exported as a proper YAML list

#### Scenario: Empty list default

- **WHEN** a JSONField has `default=list` or `default=[]`
- **THEN** YAML exports `default: []`

### Requirement: Dictionary Field Option Inference

The system SHALL infer dictionary literals used in field options, such as `default` values for JSONField or parameters with dict configuration.

#### Scenario: Dictionary default value

- **WHEN** a JSONField has `default={"key": "value", "count": 0}`
- **THEN** YAML exports:
  ```yaml
  default:
    key: value
    count: 0
  ```

#### Scenario: Empty dict default

- **WHEN** a field has `default={}`
- **THEN** YAML exports `default: {}`

#### Scenario: Nested dictionary structure

- **WHEN** a field has `default={"config": {"timeout": 30, "retry": true}}`
- **THEN** the nested structure is properly inferred and exported

### Requirement: Safe Inference with Fallback

The system SHALL attempt astroid inference for literal values but fall back to string representation when inference fails or returns non-literal types, ensuring robustness.

#### Scenario: Unresolvable reference fallback

- **WHEN** a field option references an imported constant that cannot be inferred
- **THEN** the system exports the reference as a string (e.g., `"MyConstants.DEFAULT_VALUE"`)

#### Scenario: Callable reference preservation

- **WHEN** a field has `default=timezone.now` (callable, not literal)
- **THEN** the system exports it as string `"timezone.now"` (not attempting to call it)

#### Scenario: Complex expression fallback

- **WHEN** a field has `default=lambda: datetime.now()` or other complex expressions
- **THEN** the system exports a string representation without attempting execution

## MODIFIED Requirements

### Requirement: Field Options Parsing

The system SHALL extract all keyword arguments passed to field constructors, using astroid inference to resolve literal values (lists, tuples, dicts) where possible, and preserving complex expressions as strings for later interpretation.

#### Scenario: Common field options

- **WHEN** a field is defined as `name = models.CharField(max_length=100, null=False, blank=True, default="")`
- **THEN** all options are extracted with proper types: `{"max_length": 100, "null": False, "blank": True, "default": ""}`

#### Scenario: Complex option values with inference

- **WHEN** a field has options like `choices=[("A", "Active"), ("I", "Inactive")]`
- **THEN** the choices are inferred as a proper list structure, not a string

#### Scenario: Callable defaults

- **WHEN** a field has `default=timezone.now`
- **THEN** the default value is captured as the string `"timezone.now"` (callable reference, not inferred)
