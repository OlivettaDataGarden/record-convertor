# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

**record-convertor** is a rule-based record transformation library that converts input dicts into desired output formats using YAML or dict-based rule configurations. It normalizes records of the same data type from different sources into a single validated structure. Published on PyPI as a DataGarden Layer 0 standalone package.

## Setup

```bash
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"
```

All dependencies (runtime + dev) are defined in `pyproject.toml`. Tool configs that don't support pyproject.toml (flake8, tox) remain in `setup.cfg`.

## Commands

```bash
# Run all tests with coverage
pytest

# Run a single test file
pytest tests/test_record_convertor/test_record_convertor.py

# Run a specific test
pytest tests/test_record_convertor/test_record_convertor.py::test_name -v

# Tox environments
tox                    # Run tests across Python 3.12, 3.13, 3.14
tox -e typecheck       # mypy type checking
tox -e format          # ruff + isort formatting
tox -e lint            # flake8 linting

# Manual linting/formatting
ruff check --select I --fix && ruff format src tests
flake8 src tests
mypy --ignore-missing-imports src
```

## Code Style

- **Line length**: 88 (note: differs from DataGarden default of 110)
- **Formatter**: ruff + isort (black-compatible profile)
- **Linter**: flake8 + flake8-bugbear
- **Type checker**: mypy (Python 3.12 target)
- **Quotes**: double quotes, 4-space indentation

## Architecture

### Source layout: `src/record_convertor/`

**Entry point** (`__init__.py`): `RecordConvertor` and `RecordConvertorWithRulesDict` classes. These orchestrate the full conversion pipeline — parsing rules, iterating fields, delegating to field convertors / command processor / dataclass processor, and handling nested/recursive conversions.

### Processing pipeline

A conversion rule set defines how each output field is derived from the input record. For each rule, the convertor determines the rule type and delegates:

1. **Rules Generator** (`rules_generator/`) — Loads rules from YAML files (`RulesFromYAML`) or dicts (`RulesFromDict`) into typed `RulesDict` structures.

2. **Field Convertors** (`field_convertors/`) — Transform individual field values in-place on the input record.
   - `BaseFieldConvertor`: Composed of 4 mixins — `DataStructureConversions`, `GenericConversions`, `InPlaceBasicConversions`, `KeyValueConversions`. Supports 30+ operations (type coercion, string ops, URL ops, phone number parsing, country code mapping, math, etc.).
   - `DateFieldConvertor`: Converts between date formats (UNIX timestamps, DD-MM-YYYY, DD.MM.YYYY, YYYY_MM_DD, etc. → YYYY-MM-DD).

3. **Command Processor** (`command_processor/`) — Creates output field values from the input record using commands prefixed with `$` (e.g., `$fixed_value`, `$split_field`, `$join`, `$point` for GeoJSON, `$from_list`, `$to_list`).

4. **Dataclass Processor** (`dataclass_processor/`) — Converts records through Pydantic models or dataclasses, optionally invoking methods on instances before extracting the dict.

5. **Conditions** (`package_settings/conditions/`) — `EvaluateConditions` controls conditional rule execution based on field values (equals, contains, is_null, in_list, field_does_exist, etc.).

### Key design patterns

- **Protocol-based injection**: `RecordConvertorProtocol`, `FieldConvertorProtocol`, `DateFormatProtocol` allow custom convertor classes to be passed in.
- **JMESPath**: Used for nested field access in input records (e.g., `"item.brand.name"`).
- **Recursive processing**: Handles nested dicts and lists within records.
- **Type definitions**: `RulesDict`, `BaseRuleDict`, `FormatDateRuleDict`, `SkipRuleDict`, `DataClassRuleDict` in `package_settings/package_types.py`.

## Documentation

Sphinx-based docs live in `docs/` and are published to Read the Docs. RTD build config is in `.readthedocs.yaml`.

```bash
# Build docs locally
cd docs && sphinx-build -b html . _build/html

# Open in browser
open docs/_build/html/index.html
```

### Documentation structure

- `docs/index.rst` — Landing page with quick example
- `docs/usage.rst` — Getting started, rule types overview, protocol customization
- `docs/field-convertors.rst` — All `$convert` field conversion actions
- `docs/commands.rst` — All `$` command processors
- `docs/conditions.rst` — Condition system reference
- `docs/date-convertors.rst` — Date format conversion reference
- `docs/dataclass-processor.rst` — Dataclass/Pydantic model processing
- `docs/api.rst` — Auto-generated API reference (autodoc)
- `docs/contributing.rst`, `docs/authors.rst`, `docs/changelog.rst` — Include root-level rst files

## Dependencies

Runtime: `jmespath`, `phonenumbers`, `unidecode`, `pyyaml`, `pydantic`
