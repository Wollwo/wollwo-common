# CUSTOM_LOGGING

## HOW TO

### Bump package versions
```BASH
cd /path/to/project/custom_logging

poetry version patch  #: 0.1.0 -> 0.1.1
poetry version minor  #: 0.1.0 -> 0.2.0
poetry version major  #: 0.1.0 -> 1.1.0

#: check with
poetry version
```

### Build package
Before building bump version of package (see above or in `/path/to/project/custom_logging/pyproject.toml`).
After build check `/path/to/project/custom_logging/dist`
```BASH
cd /path/to/project/custom_logging
poetry build
```

### install package with poetry as python library
```BASH
cd /path/to/project/custom_logging
poetry install
```