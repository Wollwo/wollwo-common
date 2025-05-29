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

### Build project
Before building bump version of package (see above or in `/path/to/project/custom_logging/pyproject.toml`).
After build check `/path/to/project/custom_logging/dist`
```BASH
cd /path/to/project/custom_logging
poetry build
```

### install project with poetry as python library
```BASH
cd /path/to/project/custom_logging
poetry install
```

### add/remove library to dependency
```BASH
poetry add package_name
poetry add package_name@0.1.0  #: exact version
poetry add package_name@^0.1.0  #: greater version than 0.1.0, but less than next major version 1.0.0
poetry add package_name@<0.1.0  #: lesser version than specified
poetry remove package_name
```