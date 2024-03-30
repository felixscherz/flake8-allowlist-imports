# flake8-allowlist-imports

[![PyPI - Version](https://img.shields.io/pypi/v/flake8-allowlist-imports.svg)](https://pypi.org/project/flake8-allowlist-imports)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/flake8-allowlist-imports.svg)](https://pypi.org/project/flake8-allowlist-imports)

---

flake8 plugin which validates imports against an allowlist

## installation

`pip install flake8-allowlist-imports`

## flake8 codes

| Code   | Description                                             |
|--------|---------------------------------------------------------|
| FAI001 | third party package is not allowed by the allowlist     |

## rationale

flake8-allowlist-imports helps with constraining imports when building applications in a team

## configuration

This plugin expects a comma-separated list of package names to allow.
Packages can be specified via `--import-allowlist` or as part of the flake8 configuration:

```ini
[flake8]
import-allowlist = mypackage,requests
```

## as a pre-commit hook

See [pre-commit](https://github.com/pre-commit/pre-commit) for instructions.
Sample `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/pycqa/flake8
  rev: 7.0.0
  hooks:
    - id: flake8
      additional_dependencies: [flake8-allowlist-imports==0.1.1]
      args:
        - --import-allowlist
        - mypackage,requests
```

