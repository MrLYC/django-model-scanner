# Design Document: Django Model Scanner

## Context

Django projects often require static analysis of model definitions for various purposes:
- **Documentation**: Automatic generation of model reference docs and ER diagrams
- **Schema Evolution**: Tracking model changes over time for migration validation
- **Code Analysis**: Detecting anti-patterns, unused fields, or complex relationships
- **Migration Validation**: Comparing model definitions against actual migrations

Current approaches require executing Django code (`django.setup()`), which has significant drawbacks:
- **Performance**: Slow startup, full application initialization required
- **Side Effects**: May trigger signals, connect to databases, modify state
- **Environment Requirements**: Needs proper database configuration, settings, dependencies
- **Safety**: Cannot analyze untrusted or broken code safely

**Stakeholders**: Django developers, DevOps engineers, documentation tools, schema management systems

**Constraints**:
- Must work without Django runtime or database connection
- Must handle all Django model patterns (abstract, proxy, multi-table inheritance)
- Must support various Python import styles and aliases
- Output must be machine-readable for downstream tooling

## Goals / Non-Goals

### Goals
1. **Static Analysis**: Scan Django models using AST only, no code execution
2. **Comprehensive Coverage**: Support all field types, relationships, abstract inheritance
3. **Accurate Resolution**: Handle string references, aliases, cross-file imports correctly
4. **Structured Output**: Produce well-defined YAML schema suitable for tooling
5. **Extensibility**: Design for future enhancements (diff, metrics, ER diagrams)

### Non-Goals
1. **Runtime Validation**: Not validating model correctness or database compatibility
2. **Migration Generation**: Not creating or comparing Django migrations
3. **Proxy/Multi-table Inheritance**: Focus on abstract inheritance first (can add later)
4. **Dynamic Fields**: Not handling programmatically generated fields or metaclass magic
5. **Performance Optimization**: Initial focus on correctness over speed

## Technical Decisions

### Decision 1: Pylint + Astroid Framework

**Choice**: Build as a pylint checker using astroid for AST analysis

**Rationale**:
- **Astroid Inference**: Superior type inference compared to raw AST, resolves imports/aliases automatically
- **Existing Ecosystem**: Pylint integration means standard tooling, CI/CD compatibility
- **Visitor Pattern**: Clean architecture for traversing and analyzing class definitions
- **No Django Import**: Astroid can analyze Django source without importing it

**Alternatives Considered**:
- **Raw AST**: Too low-level, manual import resolution is error-prone
- **LibCST**: Preserves formatting but weaker inference, no Django-specific knowledge
- **Standalone Tool**: More flexibility but reinvents wheel for plugin system, configuration

**Trade-offs**:
- ✅ Powerful inference, established patterns
- ✅ Easy integration into existing lint workflows
- ❌ Tied to pylint release cycles
- ❌ Learning curve for astroid APIs

### Decision 2: Two-Pass Scanning for Inheritance

**Choice**: First pass collects all models, second pass merges abstract inheritance

**Rationale**:
- **Forward References**: Abstract parent may be defined after concrete child in file
- **Cross-File Inheritance**: Parent in one module, child in another
- **Correct MRO**: Need full model graph to compute Method Resolution Order for field merging

**Implementation**:
```python
# Pass 1: Collect all models
for file in project:
    for class in file.classes:
        if is_django_model(class):
            models[class.qname()] = parse_model(class)

# Pass 2: Merge inheritance
for model_name, model in models.items():
    ancestors = get_abstract_ancestors(model)
    merge_abstract_fields(model, ancestors, models)
```

**Alternatives Considered**:
- **Single Pass**: Fails on forward references and cross-file inheritance
- **Lazy Resolution**: Complex state management, harder to debug

**Trade-offs**:
- ✅ Handles all inheritance patterns correctly
- ✅ Clean separation of concerns
- ❌ Requires full project scan before output
- ❌ Slightly higher memory usage

### Decision 3: String Representation for Option Values

**Choice**: Store field options as string representations during parsing, normalize during export

**Rationale**:
- **Preserve Intent**: Keep original expressions for debugging (e.g., `timezone.now` not `<function>`)
- **Simplify Parsing**: Avoid complex value inference during model scanning
- **Deferred Conversion**: YAML export is single point for type normalization

**Implementation**:
```python
# Parsing: store as strings
options = {kw.arg: kw.value.as_string() for kw in call.keywords}

# Export: normalize types
def normalize_value(value_str):
    if value_str == "True": return True
    if value_str == "False": return False
    if value_str == "None": return None
    if value_str.isdigit(): return int(value_str)
    return value_str.strip('"\'')
```

**Alternatives Considered**:
- **Eager Evaluation**: Infer types during parsing (complex, error-prone)
- **Keep All Strings**: Less useful for downstream tools expecting typed data

**Trade-offs**:
- ✅ Simple parsing logic, robust to edge cases
- ✅ Preserves debugging information
- ❌ Requires normalization pass during export
- ❌ May lose precision for complex expressions

### Decision 4: Separate Fields and Relationships Sections

**Choice**: Split YAML output into `fields` (all fields) and `relationships` (FK/M2M metadata)

**Rationale**:
- **Dual Nature**: Relationship fields are both fields (with type, null, etc.) and relationships (target, cascade)
- **Query Convenience**: Tools can process all fields or just relationships independently
- **Schema Clarity**: Explicit separation makes output structure more understandable

**Example Output**:
```yaml
app.models.Article:
  fields:
    author:
      type: ForeignKey
      null: false
  relationships:
    author:
      type: ForeignKey
      to: app.models.User
      on_delete: CASCADE
      related_name: articles
```

**Alternatives Considered**:
- **Unified Section**: Single fields section with nested relationship info (cluttered)
- **Relationships Only**: Omit FK/M2M from fields (loses constraint information)

**Trade-offs**:
- ✅ Clear separation of concerns
- ✅ Supports both field-level and relationship-level queries
- ❌ Slight duplication (field name appears twice)
- ❌ More complex schema

### Decision 5: Qualified Names for Target Resolution

**Choice**: Always resolve model references to fully qualified names (`app.models.ModelName`)

**Rationale**:
- **Unambiguous**: No confusion about which `User` model when multiple apps have one
- **Portable**: References work across modules without import context
- **Tooling-Friendly**: Downstream tools can locate models without inference

**Resolution Logic**:
```python
def resolve_target(target_str, current_app):
    if target_str == "self":
        return current_model_qname
    if "." in target_str:
        return f"{target_str.rsplit('.', 1)[0]}.models.{target_str.split('.')[-1]}"
    else:
        return f"{current_app}.models.{target_str}"
```

**Alternatives Considered**:
- **Keep Original Strings**: Less useful, requires consumers to re-resolve
- **Relative References**: Fragile across module moves

**Trade-offs**:
- ✅ Unambiguous references
- ✅ Easy for tools to validate/traverse
- ❌ Assumes standard Django app structure (`app.models`)
- ❌ May break with non-standard layouts (can handle as edge case)

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    Pylint Framework                     │
│  (drives file traversal, AST loading via astroid)       │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│              DjangoModelChecker (checker.py)            │
│  - visit_classdef(): dispatches to model detection      │
│  - close(): triggers YAML export after all files        │
└────────────────────────┬────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ▼               ▼               ▼
┌─────────────┐  ┌──────────────┐  ┌──────────────┐
│ ast_utils   │  │ model_parser │  │ export       │
│             │  │              │  │              │
│ - is_model  │  │ - parse_model│  │ - to_yaml    │
│ - is_field  │  │ - parse_field│  │ - normalize  │
│ - get_meta  │  │ - merge_inh. │  │              │
└─────────────┘  └──────────────┘  └──────────────┘
```

### Module Responsibilities

- **checker.py**: Pylint integration, orchestrates scanning, accumulates models
- **ast_utils.py**: Low-level astroid helpers, inference wrappers, safe node access
- **model_parser.py**: Model/field parsing, inheritance merging, relationship resolution
- **export.py**: YAML generation, value normalization, output formatting

### Data Flow

1. **Pylint** loads each Python file as astroid AST
2. **Checker** visits each `ClassDef` node
3. **ast_utils** determines if class is Django model
4. **model_parser** extracts fields, options, metadata → dict
5. **Checker** accumulates models in `self.models` dict
6. **After all files**: checker.close() calls export
7. **export** normalizes values, formats structure, writes YAML

## Risks / Trade-offs

### Risk: Astroid Inference Failures

**Description**: Astroid may fail to infer types for complex import patterns or dynamic code

**Mitigation**:
- Wrap all inference calls in try/except, continue on failure
- Log warnings for unresolved imports (verbose mode)
- Provide manual override configuration for problematic imports

**Fallback**: If inference fails, fall back to literal string matching for common patterns

### Risk: Non-Standard Django Structures

**Description**: Projects with custom model base classes, non-standard app layouts

**Mitigation**:
- Support configuring custom model base class QNames
- Handle both `app.models` and `app.models.submodule` structures
- Document known limitations for exotic patterns

**Acceptance**: 95% coverage is acceptable for initial version

### Risk: Performance on Large Projects

**Description**: Full project scan + two-pass processing may be slow on 1000+ model projects

**Mitigation**:
- Profile on large real-world Django projects (e.g., Sentry, GitLab)
- Add incremental mode: only scan modified files (future)
- Cache astroid inference results where possible

**Threshold**: <10 seconds for 500 models is acceptable

### Risk: YAML Output Schema Evolution

**Description**: Adding new features may break existing consumers of YAML

**Mitigation**:
- Version the YAML schema with metadata field: `_version: "1.0"`
- Use additive changes only (new optional fields)
- Provide schema migration tools if breaking changes needed

**Policy**: Treat YAML format as public API with semantic versioning

## Migration Plan

### Phase 1: Initial Implementation (MVP)
- Concrete models with basic fields (CharField, IntegerField, etc.)
- ForeignKey relationships
- Abstract inheritance (single-level)
- YAML export to file

### Phase 2: Advanced Features
- OneToOneField, ManyToManyField support
- Multi-level abstract inheritance
- Relationship options (related_name, through, on_delete)
- Configuration options (output path, custom base classes)

### Phase 3: Robustness
- Comprehensive error handling
- Verbose debugging mode
- Edge case testing (circular refs, dynamic fields)
- Documentation and examples

### Phase 4: Extensibility
- Plugin system for custom field types
- Hooks for downstream tools (diff, ER diagram)
- JSON output option
- API for programmatic usage

### Rollback Strategy

No migration needed (new functionality). If issues arise:
1. Document known limitations
2. Provide workarounds for unsupported patterns
3. Iterate based on real-world feedback

## Extensibility Strategy

### Hook Points for Future Features

1. **Custom Field Handlers**: Register field type parsers for third-party field packages
   ```python
   registry.register_field_type("django_extensions.db.models.UUIDField", parse_uuid_field)
   ```

2. **Output Formats**: Pluggable exporters for JSON, SQL, ER diagram DSL
   ```python
   exporter = get_exporter(format="json")
   exporter.export(models)
   ```

3. **Post-Processing**: Hooks to modify parsed models before export
   ```python
   def add_metrics(model):
       model["_metrics"] = {"field_count": len(model["fields"])}
   
   checker.add_post_processor(add_metrics)
   ```

4. **Diff Generation**: Compare two model sets for schema evolution
   ```python
   diff = compare_models(old_yaml, new_yaml)
   ```

### Planned Extensions (Not in Initial Scope)

- **ER Diagram Generation**: Convert YAML to Mermaid/GraphViz
- **Migration Validator**: Compare models against migration files
- **Complexity Metrics**: Field count, relationship depth, inheritance levels
- **Schema Linting**: Detect anti-patterns (no `on_delete`, missing indexes)

## Open Questions

1. **Q**: Should we support proxy models in initial version?
   **A**: No, defer to Phase 2. Proxy models are less common and add complexity.

2. **Q**: How to handle programmatically generated fields (e.g., from metaclasses)?
   **A**: Out of scope. Document as limitation. Static analysis can't detect runtime magic.

3. **Q**: Should we validate relationship targets exist?
   **A**: Yes, but only log warnings. Don't fail on broken references (project may be incomplete).

4. **Q**: What about custom managers and querysets?
   **A**: Out of scope for MVP. Future extension point for documenting model API.

5. **Q**: Support for Django 3.2, 4.0, 4.2, 5.0 simultaneously?
   **A**: Yes. Astroid doesn't execute code, so version differences are minimal. Test on latest LTS (3.2, 4.2, 5.0).
