# Contributing to TodoSync

## Overview

Welcome to the TodoSync project! We appreciate your interest in contributing to this cross-platform todo application with real-time synchronization capabilities. This guide will help you get started with contributing to our project.

## How to Contribute

There are many ways you can contribute to TodoSync:

1. **Reporting Bugs**: Help us find and fix issues
2. **Suggesting Features**: Propose new enhancements for the application
3. **Writing Code**: Contribute to the core application
4. **Documentation**: Improve our documentation resources  
5. **Testing**: Verify fixes and new features work properly
6. **Promotion**: Spread the word about TodoSync

## Reporting Bugs

### Before Submitting a Bug Report

1. **Check Existing Issues**: Search the issue tracker to see if your bug has already been reported
2. **Verify on Latest Version**: Ensure you're testing against the most recent version
3. **Isolate the Problem**: Try to reproduce the issue in isolation

### How to Submit a Bug Report

When submitting a bug report, please include:

- **Environment Details**:
  - Operating system and version 
  - Browser version (if web-based)
  - Device type and specifications

- **Steps to Reproduce**:
  - Clear, step-by-step instructions
  - Include any relevant code snippets

- **Expected vs Actual Behavior**: 
  - What you expected to happen  
  - What actually happened

- **Screenshots/Logs**: Any relevant screenshots or log files

### Example Bug Report Format

```
### Bug Title
Brief description of the issue

### Environment
- OS: [e.g., Ubuntu 22.04, Windows 11, Android 12]
- Browser: [if applicable]
- App Version: [version number]

### Steps to Reproduce
1. Step 1
2. Step 2  
3. Step 3

### Expected Behavior
What should happen

### Actual Behavior
What actually happens

### Screenshots
[Attach relevant screenshots if applicable]
```

## Feature Requests

We welcome suggestions for new features that would enhance the TodoSync experience:

1. **Feature Description**: Clearly describe what you'd like to see implemented
2. **Use Case**: Explain when and why this feature would be useful
3. **Implementation Considerations**: Any thoughts on how it might work
4. **Priority Level**: High, Medium, or Low

## Code Contribution Process

### Fork and Clone the Repository

```bash
# Fork the repository on GitHub
git clone https://github.com/<your-username>/TodoApp.git
cd TodoApp
```

### Set Up Development Environment

1. **Install Prerequisites**:
   - Node.js (v16 or higher) 
   - Rust toolchain
   - Python 3.7+ (for backend)
   - Android development tools (for mobile builds)

2. **Install Dependencies**:
```bash
# Frontend dependencies
npm install

# Backend dependencies  
pip install -r requirements.txt
```

### Development Guidelines

1. **Code Style**: Follow existing code style conventions
2. **Documentation**: Update documentation for new features
3. **Testing**: Add tests for your changes
4. **Commit Messages**: Use descriptive commit messages following conventional commits

### Branch Strategy

1. **Create Feature Branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Your Changes**: Implement your solution following project conventions

3. **Test Thoroughly**: Ensure existing tests pass and add new tests as needed

4. **Commit Your Changes**: 
   ```bash
   git add .
   git commit -m "feat: add new feature"  # or "fix:", "docs:", etc.
   ```

5. **Push to Your Fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create Pull Request**: Submit PR against the main branch

### Code Review Process

1. **Quality Assurance**: Ensure code meets project standards
2. **Testing**: All changes must be tested (unit, integration, end-to-end)
3. **Documentation**: Update relevant documentation files
4. **Peer Review**: Changes reviewed by maintainers before merging

## Testing Guidelines

### Unit Tests

All contributions should include unit tests:

1. **Backend Tests** (`tests/backend/`):
   - Test conflict resolution logic
   - Test database models  
   - Test API endpoints
   - Test WebSocket communication

2. **Frontend Tests** (`tests/frontend/`):
   - Test API wrapper functions
   - Test offline queue system  
   - Test WebSocket connection logic

### Running Tests

```bash
# Run all tests
npm test

# Run backend tests specifically
python -m pytest tests/backend/

# Run frontend tests
npm run test:frontend
```

### End-to-End Testing

1. **Integration Testing**: Test full synchronization workflows
2. **Cross-platform Testing**: Verify on all supported platforms
3. **Edge Case Testing**: Test network interruptions, concurrent writes

## Documentation Contribution

We value high-quality documentation. Contributing to documentation includes:

1. **Technical Documentation**: API references, implementation details  
2. **User Guides**: How-to guides for common tasks
3. **Troubleshooting**: Common issues and solutions
4. **Examples**: Practical code examples and use cases

### Documentation Structure

Documentation files should be:
- Well-organized in clear sections
- Include practical examples where applicable
- Use consistent formatting
- Be updated when features change

## Code of Conduct

This project follows a Code of Conduct to ensure a welcoming environment for all contributors:

1. **Be Respectful**: Treat all people with respect and courtesy
2. **Be Inclusive**: Welcome diverse perspectives and experiences  
3. **Be Collaborative**: Work together to achieve common goals
4. **Be Constructive**: Provide helpful feedback rather than criticism
5. **Be Professional**: Maintain professional standards in communication

## License

By contributing to TodoSync, you agree that your contributions will be licensed under the MIT License.

## Contact

If you have questions about contributing:

- **GitHub Issues**: Use the issue tracker for bug reports and feature requests
- **Discussion Forum**: Join our community discussions  
- **Email**: Contact the maintainers directly

Thank you for helping improve TodoSync!