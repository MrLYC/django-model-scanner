# Add Django Model Scanner

## Why

Django projects often need static analysis of model definitions for documentation, schema evolution tracking, ER diagram generation, and migration validation. Existing solutions require executing Django code (`django.setup()`), which is slow, has side effects, and fails in environments without proper database configuration. A static analysis approach using pylint + astroid enables fast, safe model scanning without runtime execution.

## What Changes

- **Static Model Detection**: Identify Django Model classes through AST analysis using astroid's inference engine, supporting aliases and cross-file imports
- **Field Parsing**: Extract field types, options, and constraints from Django field definitions (CharField, ForeignKey, etc.)
- **Relationship Resolution**: Parse ForeignKey, OneToOneField, and ManyToManyField relationships with proper target resolution
- **Abstract Model Inheritance**: Handle abstract base models and field inheritance to child models
- **YAML Export**: Output structured YAML representation of all discovered models with fields, relationships, and metadata
- **Pylint Integration**: Implement as a pylint checker for seamless integration with existing linting workflows

## Impact

### New Capabilities
- `model-detection`: Identifies Django models via static analysis
- `field-parsing`: Extracts field definitions and options
- `relationship-resolution`: Resolves inter-model relationships
- `abstract-inheritance`: Handles abstract model field inheritance
- `yaml-export`: Generates structured YAML output

### Affected Code
- New package structure under `django_model_scanner/`
- New files: `checker.py`, `model_parser.py`, `ast_utils.py`, `export.py`
- Updated: `pyproject.toml` (add dependencies: astroid, PyYAML)
- Updated: `README.md` (usage documentation)

### Breaking Changes
None (new functionality)

## Success Criteria

1. Can scan Django projects without importing or executing code
2. Correctly identifies models with abstract inheritance
3. Resolves ForeignKey/M2M relationships including string references
4. Outputs valid YAML matching the documented schema
5. Handles edge cases: custom base classes, multiple inheritance, dynamic fields
