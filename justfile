import "/Users/maartenderuyter/Documents/dg-development/dg_justfile/Justfile"

# Local vars:
IS_PACKAGE := "true"
COMMIT_PREFIX := "DGRC"
REPO_NAME := "record-convertor"


tox:
    uv run tox
