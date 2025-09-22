# Python Best Practices for VarLabzBot

This document outlines the best practices for writing Python code in the VarLabzBot project. These guidelines ensure code quality, readability, and maintainability.

## Code Style (PEP 8)

Follow PEP 8, the official Python style guide:

- **Indentation**: Use 4 spaces per indentation level. Never mix tabs and spaces.
- **Line Length**: Limit lines to 79 characters for code, 72 for docstrings and comments.
- **Naming Conventions**:
  - Variables and functions: `snake_case`
  - Classes: `PascalCase`
  - Constants: `UPPER_CASE`
- **Imports**: Place imports at the top of the file, grouped as standard library, third-party, and local imports. Use absolute imports.

Example:
```python
import os
import sys
from typing import List, Optional

from telegram import Update
from telegram.ext import Application, CommandHandler

from .local_module import some_function
```

## Documentation

- Write docstrings for all public modules, functions, classes, and methods following PEP 257.
- Keep docstrings up-to-date with the code.
- Use type hints for function parameters and return types.

Example:
```python
def greet_user(name: str) -> str:
    """
    Generate a greeting message for the user.

    Args:
        name (str): The name of the user.

    Returns:
        str: A personalized greeting message.
    """
    return f"Hello, {name}!"
```

## Code Quality

- Use linters and formatters: Black for auto-formatting, Flake8 or Pylint for linting.
- Write clean, readable code. Prefer explicit over implicit.
- Avoid global variables; use class attributes or pass parameters instead.
- Handle exceptions properly; don't use bare `except:` clauses.

Example of good error handling:
```python
try:
    result = risky_operation()
except ValueError as e:
    logger.error(f"Invalid value: {e}")
    return None
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    raise
```

## Efficiency and Best Practices

- Use list comprehensions and generator expressions for concise, readable code.
- Prefer `enumerate()` over manual indexing.
- Use context managers (`with` statements) for resource management.
- Write unit tests for new functionality.

Example of list comprehension:
```python
# Good
squares = [x**2 for x in range(10) if x % 2 == 0]

# Avoid
squares = []
for x in range(10):
    if x % 2 == 0:
        squares.append(x**2)
```

## Project-Specific Rules

- For Telegram bot interactions, always validate user input.
- Use logging instead of print statements for debugging and monitoring.
- Keep sensitive information (API keys, tokens) in environment variables or secure config files.

## Tools and Dependencies

- Use `uv` for dependency management (as indicated by `uv.lock`).
- Update `pyproject.toml` for new dependencies.
- Run tests with `pytest` or similar before committing.

## References

- [PEP 8 – Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [PEP 257 – Docstring Conventions](https://peps.python.org/pep-0257/)
- [The Hitchhiker's Guide to Python](https://docs.python-guide.org/)
