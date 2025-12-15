# Implementation Tasks

## 1. Add AST Utility for Literal Inference

- [x] 1.1 Create `infer_literal_value(node)` function in `ast_utils.py`
  - Use `node.infer()` to get inferred value
  - Handle `astroid.Const` nodes (strings, numbers, booleans, None)
  - Handle `astroid.List` nodes recursively
  - Handle `astroid.Tuple` nodes recursively
  - Handle `astroid.Dict` nodes recursively
  - Return original string representation on inference failure
- [x] 1.2 Add unit tests for `infer_literal_value()` with various literal types
- [x] 1.3 Test fallback behavior for unresolvable references

## 2. Update Model Parser for Base Class Tracking

- [x] 2.1 Modify `parse_model()` in `model_parser.py` to collect base class qualified names
  - Iterate through `class_node.bases`
  - Use astroid inference to resolve base class qualified names
  - Filter out `django.db.models.Model` itself
  - Store in `model["bases"]` list
- [x] 2.2 Add test cases for models with abstract inheritance
- [x] 2.3 Add test cases for models with multiple inheritance
- [x] 2.4 Add test case for direct Model inheritance (empty bases list)

## 3. Enhance Field Option Inference

- [x] 3.1 Update `parse_field()` in `model_parser.py` to use `infer_literal_value()`
  - For each keyword argument value node, attempt inference
  - Use inferred value if successful, otherwise use `safe_as_string()`
  - Special handling for `choices` option
- [x] 3.2 Add test cases for choices with tuples
- [x] 3.3 Add test cases for choices with integer keys
- [x] 3.4 Add test cases for default list/dict values
- [x] 3.5 Add test case for fallback to string representation

## 4. Update YAML Export for New Data Structures

- [x] 4.1 Modify `format_model_output()` in `export.py` to include `bases` field
  - Add `bases` to output dictionary after `abstract`
  - Ensure empty list `[]` is exported for models without custom bases
- [x] 4.2 Update `normalize_value()` to handle lists and tuples
  - Check if value is already a list/tuple/dict (from inference)
  - If so, recursively normalize nested values
  - Otherwise, apply existing string normalization
- [x] 4.3 Add `format_choices()` helper function for choices formatting
  - Convert choices tuples to lists for YAML readability
  - Handle nested/grouped choices
- [x] 4.4 Update tests to verify bases field export
- [x] 4.5 Update tests to verify choices as YAML lists

## 5. Update Example Models and Documentation

- [x] 5.1 Add a model with choices field to `examples/blog/models.py`
- [x] 5.2 Regenerate example YAML output
- [x] 5.3 Update README.md example YAML to show `bases` field
- [x] 5.4 Update README.md example YAML to show properly formatted choices

## 6. Integration Testing

- [x] 6.1 Test full scanner flow with inheritance tracking
- [x] 6.2 Test full scanner flow with choices inference
- [x] 6.3 Verify YAML output is valid and parseable
- [x] 6.4 Test fallback behavior for complex expressions
- [x] 6.5 Test performance impact (should be minimal)

## 7. Edge Cases and Error Handling

- [x] 7.1 Test with circular inheritance (should be handled by astroid)
- [x] 7.2 Test with imported base classes from other modules
- [x] 7.3 Test with unresolvable choice constants
- [x] 7.4 Test with lambda/callable defaults
- [x] 7.5 Ensure no regression in existing field parsing
