# Contributing to Telegram Polling Bot Framework

Thank you for your interest in contributing to the Telegram Polling Bot Framework! This document provides guidelines for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

This project follows a simple code of conduct:

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Keep discussions technical and relevant

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Set up the development environment
4. Create a feature branch
5. Make your changes
6. Test your changes
7. Submit a pull request

## How to Contribute

### Reporting Bugs

Before reporting a bug, please:

1. Check if the issue already exists in the [Issues](https://github.com/yourusername/telegram-polling-bot/issues) section
2. Ensure you're using the latest version
3. Test with minimal configuration to isolate the issue

When reporting a bug, include:

- Clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Environment details (Python version, OS, etc.)
- Relevant logs or error messages

### Suggesting Features

Feature requests are welcome! Please:

1. Check if the feature request already exists
2. Provide a clear description of the feature
3. Explain the use case and benefits
4. Consider backward compatibility

### Contributing Code

We welcome code contributions for:

- Bug fixes
- New features
- Performance improvements
- Documentation improvements
- Test coverage improvements

## Development Setup

### Prerequisites

- Python 3.8 or higher
- MongoDB (for database features)
- Telegram Bot Token (for testing)

### Setup Steps

```bash
# Clone your fork
git clone https://github.com/yourusername/telegram-polling-bot.git
cd telegram-polling-bot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # If exists

# Copy environment template
cp .env.example .env
# Edit .env with your test credentials

# Run tests to ensure everything works
python -m pytest tests/
```

## Coding Standards

### Python Style Guide

We follow [PEP 8](https://pep8.org/) with some exceptions:

- Line length: 100 characters (instead of 79)
- Use double quotes for strings
- Use f-strings for string formatting

### Code Formatting

We use these tools for code formatting:

```bash
# Install formatting tools
pip install black isort flake8

# Format code
black .
isort .

# Check style
flake8 .
```

### Type Hints

Use type hints for all new code:

```python
from typing import Dict, List, Optional

def process_votes(votes: List[Dict], user_id: int) -> Optional[Dict]:
    """Process user votes and return analytics."""
    pass
```

### Docstrings

Use Google-style docstrings:

```python
def calculate_weighted_votes(poll_id: str, threshold: float = 0.7) -> Dict:
    """Calculate weighted votes for a poll.
    
    Args:
        poll_id: The poll identifier
        threshold: Bias threshold for weighting
        
    Returns:
        Dictionary containing weighted vote results
        
    Raises:
        ValueError: If poll_id is invalid
    """
    pass
```

## Testing

### Test Structure

Tests are organized as follows:

```
tests/
├── unit/           # Unit tests for individual functions
├── integration/    # Integration tests for workflows
├── fixtures/       # Test data and fixtures
└── conftest.py     # Pytest configuration
```

### Writing Tests

Use pytest for all tests:

```python
import pytest
from unittest.mock import Mock, AsyncMock
from polling_bot import BotManager

class TestBotManager:
    def test_poll_initialization(self):
        """Test poll payload initialization."""
        bot = BotManager()
        assert bot.poll_payload['total_votes'] == 0
    
    @pytest.mark.asyncio
    async def test_poll_creation(self):
        """Test poll creation workflow."""
        # Test implementation
        pass
```

### Running Tests

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=.

# Run specific test file
python -m pytest tests/unit/test_bot_manager.py

# Run with verbose output
python -m pytest -v
```

### Test Coverage

Aim for at least 80% test coverage. Check coverage with:

```bash
python -m pytest --cov=. --cov-report=html
# Open htmlcov/index.html to view detailed coverage
```

## Documentation

### Code Documentation

- All public functions must have docstrings
- Include examples in docstrings for complex functions
- Update API documentation when adding new features

### README Updates

When adding features, update:

- Feature list in README.md
- Configuration options
- Usage examples
- API documentation

### Example Documentation

Include examples for new features:

```python
# examples/new_feature.py
"""
Example demonstrating the new feature.
"""

def example_usage():
    """Show how to use the new feature."""
    pass
```

## Pull Request Process

### Before Submitting

1. Ensure all tests pass
2. Update documentation
3. Add tests for new features
4. Follow coding standards
5. Update CHANGELOG.md if applicable

### PR Guidelines

1. **Title**: Use descriptive title (e.g., "Add weighted voting feature")
2. **Description**: Explain what the PR does and why
3. **Breaking Changes**: Clearly mark any breaking changes
4. **Related Issues**: Reference related issues with "Fixes #123"

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] Added tests for new features
- [ ] Updated documentation

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or clearly documented)
```

### Review Process

1. All PRs require at least one review
2. Address all review comments
3. Ensure CI checks pass
4. Maintainer will merge after approval

## Release Process

Releases follow semantic versioning (SemVer):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

1. Update version numbers
2. Update CHANGELOG.md
3. Create release tag
4. Deploy to PyPI (if applicable)

## Getting Help

If you need help:

1. Check the documentation
2. Search existing issues
3. Ask in discussions
4. Contact maintainers

## Recognition

Contributors will be:

- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Given appropriate credit

Thank you for contributing to the Telegram Polling Bot Framework!
