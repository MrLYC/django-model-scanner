# Implementation Tasks

## 1. Project Setup and Dependencies

- [ ] 1.1 Update pyproject.toml with required dependencies (astroid, PyYAML, pylint>=4.0)
- [ ] 1.2 Create package structure: `django_model_scanner/__init__.py`
- [ ] 1.3 Configure package exports and version metadata

## 2. AST Utilities Module

- [ ] 2.1 Create `ast_utils.py` with astroid helper functions
- [ ] 2.2 Implement `is_django_model(class_node)` - checks inheritance from `django.db.models.base.Model`
- [ ] 2.3 Implement `is_abstract_model(class_node)` - inspects Meta class for `abstract = True`
- [ ] 2.4 Implement `is_django_field(call_node)` - identifies Field subclasses via inference
- [ ] 2.5 Implement `get_meta_option(class_node, option_name)` - extracts Meta class attributes
- [ ] 2.6 Add error handling for inference failures and missing attributes
- [ ] 2.7 Write unit tests for AST utilities with fixture files

## 3. Model Parser Module

- [ ] 3.1 Create `model_parser.py` with model analysis functions
- [ ] 3.2 Implement `parse_field(assign_node)` - extracts field name, type, args, options
- [ ] 3.3 Implement `normalize_relation(field_type, args, options)` - creates relationship metadata
- [ ] 3.4 Implement `parse_model(class_node)` - collects all fields and metadata for one model
- [ ] 3.5 Implement `merge_abstract_fields(model, ancestors, model_map)` - handles field inheritance
- [ ] 3.6 Implement `resolve_target_model(target_ref, current_app)` - resolves string references to qualified names
- [ ] 3.7 Implement `extract_table_name(class_node, app_label)` - gets db_table or derives default
- [ ] 3.8 Write unit tests for model parser with various field types and inheritance patterns

## 4. YAML Export Module

- [ ] 4.1 Create `export.py` with YAML generation functions
- [ ] 4.2 Implement `normalize_value(value_str)` - converts AST strings to proper Python types (bool, int, None)
- [ ] 4.3 Implement `format_field_options(options_dict)` - normalizes field option values
- [ ] 4.4 Implement `format_model_output(model_dict)` - structures model data for YAML
- [ ] 4.5 Implement `export_to_yaml(models_dict, output_path)` - writes YAML with proper formatting
- [ ] 4.6 Add configuration for output path (default: `django_models.yaml`)
- [ ] 4.7 Write unit tests for YAML export with expected output fixtures

## 5. Pylint Checker Integration

- [ ] 5.1 Create `checker.py` implementing `BaseChecker` from pylint
- [ ] 5.2 Implement `DjangoModelChecker` class with IAstroidChecker interface
- [ ] 5.3 Add `__init__` to initialize models dictionary for accumulation
- [ ] 5.4 Implement `visit_classdef` to detect and parse Django models
- [ ] 5.5 Implement `close` method to trigger YAML export after all files scanned
- [ ] 5.6 Register checker with pylint plugin system
- [ ] 5.7 Add configuration options (output path, verbosity)
- [ ] 5.8 Write integration tests using pylint's test framework

## 6. Abstract Inheritance Handling

- [ ] 6.1 Extend `parse_model` to track ancestor classes
- [ ] 6.2 Implement two-pass scanning: first collect all models, then merge inheritance
- [ ] 6.3 Implement `get_all_abstract_ancestors(class_node)` - traverses full inheritance chain
- [ ] 6.4 Implement field override logic (child fields override parent fields by name)
- [ ] 6.5 Preserve field order according to MRO
- [ ] 6.6 Write tests for multi-level abstract inheritance and diamond patterns

## 7. Relationship Resolution

- [ ] 7.1 Implement relationship field detection in `parse_field`
- [ ] 7.2 Handle string target references: `"self"`, `"ModelName"`, `"app.ModelName"`
- [ ] 7.3 Extract relationship options: `on_delete`, `related_name`, `through`, `to_field`
- [ ] 7.4 Create separate relationships section in model output
- [ ] 7.5 Write tests for various relationship patterns (FK, O2O, M2M, self-referential)

## 8. Documentation and Usage

- [ ] 8.1 Write comprehensive README.md with installation instructions
- [ ] 8.2 Document usage: `pylint project_path --load-plugins=django_model_scanner.checker --disable=all`
- [ ] 8.3 Add examples of YAML output format
- [ ] 8.4 Document configuration options
- [ ] 8.5 Add troubleshooting section for common issues
- [ ] 8.6 Create example Django project for testing

## 9. Testing and Validation

- [ ] 9.1 Create test fixtures: sample Django models with various patterns
- [ ] 9.2 Write integration test that scans test fixtures and validates YAML output
- [ ] 9.3 Test edge cases: no models, abstract-only models, circular references
- [ ] 9.4 Test various import styles and aliases
- [ ] 9.5 Validate YAML output against expected schema
- [ ] 9.6 Test on real Django projects (if available)

## 10. Error Handling and Robustness

- [ ] 10.1 Add graceful handling for missing imports
- [ ] 10.2 Handle malformed field definitions without crashing
- [ ] 10.3 Log warnings for unresolvable relationships
- [ ] 10.4 Add verbose mode for debugging inference issues
- [ ] 10.5 Ensure no Django runtime dependencies are imported

## 11. Performance and Extensibility

- [ ] 11.1 Optimize astroid inference calls (cache where possible)
- [ ] 11.2 Document extension points for custom field types
- [ ] 11.3 Add hooks for future features (ER diagram, diff, metrics)
- [ ] 11.4 Profile on large Django projects and optimize bottlenecks

## 12. Final Validation and Release Preparation

- [ ] 12.1 Run full test suite and ensure 100% pass rate
- [ ] 12.2 Validate on multiple Django versions (3.2, 4.0, 4.2, 5.0)
- [ ] 12.3 Check code quality with linters (pylint, mypy, black)
- [ ] 12.4 Verify YAML output is valid and matches specification
- [ ] 12.5 Update version number and changelog
- [ ] 12.6 Create release tag and publish to PyPI (if public)
