# Contributing to PMO Recovery Coach Bot

Thank you for your interest in contributing to this project! This bot helps people in their recovery journey from PMO addiction, and every contribution makes a meaningful impact.

## 🤝 How to Contribute

### Types of Contributions

1. **Code Contributions**
   - Bug fixes
   - New features
   - Performance improvements
   - Code refactoring

2. **Content Contributions**
   - Motivational quotes
   - Coping strategies
   - Educational content
   - Translation

3. **Documentation**
   - README improvements
   - Code documentation
   - Deployment guides
   - User guides

4. **Testing**
   - Bug reports
   - Feature testing
   - User experience feedback

## 🚀 Getting Started

1. **Fork the repository**
2. **Clone your fork:**
   ```bash
   git clone https://github.com/your-username/pmo-recovery-bot.git
   cd pmo-recovery-bot
   ```

3. **Setup development environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

4. **Create .env file:**
   ```bash
   cp .env.example .env
   # Add your test bot token
   ```

## 📝 Development Guidelines

### Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions small and focused

### Code Quality Tools

```bash
# Format code
black .

# Lint code
flake8 .

# Type checking
mypy .

# Run tests
pytest
```

### Commit Messages

Use conventional commit format:
- `feat:` new feature
- `fix:` bug fix
- `docs:` documentation changes
- `style:` formatting changes
- `refactor:` code refactoring
- `test:` adding tests

Example: `feat: add streak milestone celebrations`

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test
pytest tests/test_streak_service.py
```

### Writing Tests

- Write tests for new features
- Include edge cases
- Test both success and failure scenarios
- Mock external dependencies

## 📋 Pull Request Process

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write code
   - Add tests
   - Update documentation

3. **Test your changes:**
   ```bash
   # Run tests
   pytest
   
   # Check code quality
   black . && flake8 . && mypy .
   ```

4. **Commit and push:**
   ```bash
   git add .
   git commit -m "feat: describe your changes"
   git push origin feature/your-feature-name
   ```

5. **Create Pull Request**
   - Use the PR template
   - Describe your changes
   - Link related issues
   - Add screenshots if applicable

## 🎯 Priority Areas

We especially welcome contributions in these areas:

1. **Multilingual Support**
   - Translations to other languages
   - Localization features

2. **Advanced Features**
   - Data analytics and insights
   - Habit tracking integrations
   - Community features

3. **Content Enhancement**
   - More motivational quotes
   - Scientific articles
   - Coping strategies

4. **User Experience**
   - Better navigation
   - Accessibility improvements
   - Mobile optimization

## 🔒 Sensitive Content Guidelines

Given the nature of this project:

- **No NSFW content** in any form
- **Be respectful** and supportive in all communications
- **Focus on recovery** and positive aspects
- **Maintain privacy** - no personal information in code/docs
- **Be inclusive** - welcome all backgrounds and experiences

## 📚 Resources

### Understanding PMO Recovery

- Research neuroplasticity and addiction recovery
- Understand common triggers and coping mechanisms
- Learn about support community best practices

### Technical Resources

- [Python Telegram Bot Documentation](https://python-telegram-bot.readthedocs.io/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [AsyncIO Programming](https://docs.python.org/3/library/asyncio.html)

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Environment details:**
   - Python version
   - Operating system
   - Bot version

2. **Steps to reproduce**
3. **Expected vs actual behavior**
4. **Screenshots if applicable**
5. **Relevant logs**

## 💡 Feature Requests

For new features:

1. **Check existing issues** first
2. **Describe the problem** you're solving
3. **Explain your proposed solution**
4. **Consider impact** on existing users
5. **Be open to discussion**

## 🤔 Questions?

- **Technical questions:** Open an issue with `question` label
- **General discussion:** Use GitHub Discussions
- **Security concerns:** Email maintainers directly

## 🙏 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Thanked in the community

Every contribution, no matter how small, makes a difference in someone's recovery journey. Thank you for helping! 💙

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.
