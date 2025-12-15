# Enhance YAML Output with Inheritance Tracking and Field Inference

## Why

The current YAML export has two key limitations that reduce its usefulness for understanding Django model structures:

1. **No inheritance tracking**: When a model inherits from Django Model base classes (abstract or concrete), this relationship is not visible in the YAML output. Users cannot see the inheritance chain, making it harder to understand the model's full structure and identify which models are related through inheritance.

2. **Limited field inference**: Field options like `choices` that are defined as tuples or lists are exported as raw AST string representations (e.g., `"[(1, 'Active'), (2, 'Inactive')]"`) instead of being inferred and converted to proper YAML literal values. This makes the output less readable and harder to process programmatically.

These limitations make the YAML output less useful for documentation generation, schema analysis, and tooling integration.

## What Changes

- **Add `bases` field to model metadata**: Export a list of direct Django Model base classes (fully qualified names) that each model inherits from, excluding `django.db.models.Model` itself
- **Enhance field value inference**: Use astroid's inference capabilities to resolve field options like `choices`, converting them from AST string representations to proper YAML structures (lists, tuples, dicts) when possible
- **Improve choices handling**: Export choices as structured YAML lists with tuples or list items, not as string representations
- **Handle complex literals**: Infer and export literal values for defaults, choices, validators, and other field options that use Python data structures

## Impact

**Affected specs:**
- `yaml-export`: Add inheritance tracking to model metadata section
- `field-parsing`: Enhance field option parsing to use astroid inference for literal values

**Affected code:**
- `django_model_scanner/model_parser.py`: Update `parse_model()` to collect base class names
- `django_model_scanner/export.py`: Update `normalize_value()` to handle lists/tuples, add `format_choices()` helper
- `django_model_scanner/ast_utils.py`: Add helper function `infer_literal_value()` to safely infer AST nodes

**Benefits:**
- Better model documentation showing inheritance relationships
- More readable YAML with properly formatted choices and literals
- Easier integration with diagram generators and schema analysis tools
- Improved tracking of abstract model inheritance chains

**Risks:**
- Inference may fail for complex expressions → fallback to string representation
- Additional astroid inference calls may slightly increase processing time
