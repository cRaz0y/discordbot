# Contributing to Discord Bot

Thank you for considering contributing to this Discord bot project! We welcome contributions from the community.

## How to Contribute

### Reporting Bugs

1. Check existing issues to avoid duplicates
2. Create a new issue with:
   - Clear description of the bug
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (Python version, OS, etc.)

### Suggesting Features

1. Check existing issues for similar suggestions
2. Create a new issue with:
   - Clear description of the feature
   - Use case and benefits
   - Possible implementation approach

### Code Contributions

1. **Fork the repository**
   ```bash
   git fork https://github.com/yourusername/discord-bot.git
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the existing code style
   - Add comments for complex logic
   - Update documentation if needed

4. **Test your changes**
   - Test with your own Discord bot
   - Ensure no existing functionality is broken

5. **Commit your changes**
   ```bash
   git commit -m "Add: description of your changes"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Provide clear description of changes
   - Reference any related issues
   - Include testing information

## Code Style Guidelines

### Python Style
- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings for functions and classes
- Keep functions focused and small

### Security Guidelines
- Never commit tokens or sensitive data
- Use environment variables for configuration
- Validate user inputs
- Follow Discord.py best practices

### File Organization
- Keep related functionality together
- Use appropriate file names
- Update imports when adding new modules

## Development Setup

1. **Clone your fork**
   ```bash
   git clone https://github.com/yourusername/discord-bot.git
   cd discord-bot
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your bot token
   ```

5. **Test your setup**
   ```bash
   python secure_main.py
   ```

## Pull Request Process

1. Update documentation for any new features
2. Add your changes to the changelog (if exists)
3. Ensure your code passes all existing tests
4. Request review from maintainers
5. Address any feedback promptly

## Community Guidelines

- Be respectful and constructive
- Help others learn and grow
- Follow Discord's Terms of Service
- Maintain a welcoming environment

## Getting Help

- Create an issue for questions
- Check existing documentation
- Review similar Discord bots for examples

## Recognition

Contributors will be acknowledged in:
- README.md contributors section
- Git commit history
- Release notes (for significant contributions)

Thank you for helping make this Discord bot better! 🎉
