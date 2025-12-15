# Implementation Tasks

## 1. Project Setup and Dependencies

- [x] 1.1 Update pyproject.toml with required dependencies (astroid, PyYAML, pylint>=4.0)
- [x] 1.2 Create package structure: `django_model_scanner/__init__.py`
- [x] 1.3 Configure package exports and version metadata

## 2. AST Utilities Module

- [x] 2.1 Create `ast_utils.py` with astroid helper functions
- [x] 2.2 Implement `is_django_model(class_node)` - checks inheritance from `django.db.models.base.Model`
- [x] 2.3 Implement `is_abstract_model(class_node)` - inspects Meta class for `abstract = True`
- [x] 2.4 Implement `is_django_field(call_node)` - identifies Field subclasses via inference
- [x] 2.5 Implement `get_meta_option(class_node, option_name)` - extracts Meta class attributes
- [x] 2.6 Add error handling for inference failures and missing attributes
- [x] 2.7 Write unit tests for AST utilities with fixture files

## 3. Model Parser Module

- [x] 3.1 Create `model_parser.py` with model analysis functions
- [x] 3.2 Implement `parse_field(assign_node)` - extracts field name, type, args, options
- [x] 3.3 Implement `normalize_relation(field_type, args, options)` - creates relationship metadata
- [x] 3.4 Implement `parse_model(class_node)` - collects all fields and metadata for one model
- [x] 3.5 Implement `merge_abstract_fields(model, ancestors, model_map)` - handles field inheritance
- [x] 3.6 Implement `resolve_target_model(target_ref, current_app)` - resolves string references to qualified names
- [x] 3.7 Implement `extract_table_name(class_node, app_label)` - gets db_table or derives default
- [x] 3.8 Write unit tests for model parser with various field types and inheritance patterns

## 4. YAML Export Module

- [x] 4.1 Create `export.py` with YAML generation functions
- [x] 4.2 Implement `normalize_value(value_str)` - converts AST strings to proper Python types (bool, int, None)
- [x] 4.3 Implement `format_field_options(options_dict)` - normalizes field option values
- [x] 4.4 Implement `format_model_output(model_dict)` - structures model data for YAML
- [x] 4.5 Implement `export_to_yaml(models_dict, output_path)` - writes YAML with proper formatting
- [x] 4.6 Add configuration for output path (default: `django_models.yaml`)
- [x] 4.7 Write unit tests for YAML export with expected output fixtures

## 5. Pylint Checker Integration

- [x] 5.1 Create `checker.py` implementing `BaseChecker` from pylint
- [x] 5.2 Implement `DjangoModelChecker` class with IAstroidChecker interface
- [x] 5.3 Add `__init__` to initialize models dictionary for accumulation
- [x] 5.4 Implement `visit_classdef` to detect and parse Django models
- [x] 5.5 Implement `close` method to trigger YAML export after all files scanned
- [x] 5.6 Register checker with pylint plugin system
- [x] 5.7 Add configuration options (output path, verbosity)
- [x] 5.8 Write integration tests using pylint's test framework

## 6. Abstract Inheritance Handling

- [x] 6.1 Extend `parse_model` to track ancestor classes
- [x] 6.2 Implement two-pass scanning: first collect all models, then merge inheritance
- [x] 6.3 Implement `get_all_abstract_ancestors(class_node)` - traverses full inheritance chain
- [x] 6.4 Implement field override logic (child fields override parent fields by name)
- [x] 6.5 Preserve field order according to MRO
- [x] 6.6 Write tests for multi-level abstract inheritance and diamond patterns

## 7. Relationship Resolution

- [x] 7.1 Implement relationship field detection in `parse_field`
- [x] 7.2 Handle string target references: `"self"`, `"ModelName"`, `"app.ModelName"`
- [x] 7.3 Extract relationship options: `on_delete`, `related_name`, `through`, `to_field`
- [x] 7.4 Create separate relationships section in model output
- [x] 7.5 Write tests for various relationship patterns (FK, O2O, M2M, self-referential)

## 8. Documentation and Usage

- [x] 8.1 Write comprehensive README.md with installation instructions
- [x] 8.2 Document usage: `pylint project_path --load-plugins=django_model_scanner.checker --disable=all`
- [x] 8.3 Add examples of YAML output format
- [x] 8.4 Document configuration options
- [x] 8.5 Add troubleshooting section for common issues
- [x] 8.6 Create example Django project for testing

## 9. Testing and Validation

- [x] 9.1 Create test fixtures: sample Django models with various patterns
- [x] 9.2 Write integration test that scans test fixtures and validates YAML output
- [x] 9.3 Test edge cases: no models, abstract-only models, circular references
- [x] 9.4 Test various import styles and aliases
- [x] 9.5 Validate YAML output against expected schema
- [x] 9.6 Test on real Django projects (if available)

## 10. Error Handling and Robustness

- [x] 10.1 Add graceful handling for missing imports
- [x] 10.2 Handle malformed field definitions without crashing
- [x] 10.3 Log warnings for unresolvable relationships
- [x] 10.4 Add verbose mode for debugging inference issues
- [x] 10.5 Ensure no Django runtime dependencies are imported

## 11. Performance and Extensibility

- [x] 11.1 Optimize astroid inference calls (cache where possible)
- [x] 11.2 Document extension points for custom field types
- [x] 11.3 Add hooks for future features (ER diagram, diff, metrics)
- [x] 11.4 Profile on large Django projects and optimize bottlenecks

## 12. Final Validation and Release Preparation

- [x] 12.1 Run full test suite and ensure 100% pass rate
- [x] 12.2 Validate on multiple Django versions (3.2, 4.0, 4.2, 5.0)
- [x] 12.3 Check code quality with linters (pylint, mypy, black)
- [x] 12.4 Verify YAML output is valid and matches specification
- [x] 12.5 Update version number and changelog
- [x] 12.6 Create release tag and publish to PyPI (if public)
