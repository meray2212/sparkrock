# 🚀 Test Automation Framework

Automation framework for the **Pemo application** using **Playwright**, **Python**, and the **Page Object Model (POM)** pattern.  
It covers end-to-end scenarios like **user registration**, **company setup**, **bulk invitations**, and **dashboard validation**.


## 🚀 Project Overview

This project provides automated testing capabilities for the Pemo application, covering end-to-end user flows including:
- User registration and onboarding
- Company setup and configuration
- Team member management
- Bulk invitation processes
- Admin dashboard validation

## 📁 Project Structure

```
spark-rock/
├── config/                          # Configuration management
│   └── environments.py             # Environment-specific settings and URLs
├── pages/                          # Page Object Model implementations
│   ├── login_page.py              # Login page interactions
│   ├── signup_page.py             # User registration page
│   ├── company_page.py            # Company setup page
│   ├── survey_page.py             # User preferences survey
│   ├── dashboard_page.py          # Main dashboard validation
│   └── members_page.py            # Team member management
├── utils/                          # Utility functions and helpers
│   ├── api_utils.py               # API interaction utilities
│   └── data_utils.py              # Test data generation utilities
├── tests/                          # Test implementations
│   ├── test_register_company.py   # End-to-end company registration test
│   ├── test_bulk_invite.py        # Bulk invitation test
│   ├── draft_test.py              # Reference implementation (draft)
│   └── draft_bulk_invite.py      # Reference bulk invite implementation (draft)
├── pytest.ini                     # Pytest configuration
└── README.md                      # This file
```

## 🛠️ Prerequisites

Before running the tests, ensure you have the following installed:

- **Python 3.8+** - Python runtime environment
- **Node.js 16+** - Required for Playwright installation
- **Git** - Version control system

## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/meray2212/sparkrock
   cd spark-rock
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers:**
   ```bash
   playwright install
   ```

## 🔧 Configuration

### Environment Variables

The framework supports multiple environments through the `config/environments.py` file. You can run tests against different environments by setting the `ENVIRONMENT` variable:

```python
# Set environment variable
export ENVIRONMENT=dev      # Development environment
export ENVIRONMENT=staging  # Staging environment  
export ENVIRONMENT=test     # Test environment


# Default environment is "dev" if not specified
```

**Available Environments:**
- **`dev`** - Development environment (default)
- **`staging`** - Staging/QA environment
- **`test`** - Dedicated test environment


**Environment-Specific URLs:**
- **Dev:** `https://app.dev.pemo.io` / `https://api.dev.pemo.io`
- **Staging:** `https://app.staging.pemo.io` / `https://api.staging.pemo.io`
- **Test:** `https://app.test.pemo.io` / `https://api.test.pemo.io`


**Running Tests on Different Environments:**
```bash
# Development environment (default)
python3 -m pytest tests/test_register_company.py
python3 -m python3 -m pytest tests/test_bulk_invite.py 

# Staging environment
ENVIRONMENT=staging python3 -m pytest tests/test_register_company.py

# Test environment
ENVIRONMENT=test python3 -m pytest tests/test_register_company.py

# Production environment (use with caution)
ENVIRONMENT=prod python3 -m pytest tests/test_register_company.py
```

### Test Configuration

The `pytest.ini` file configures test execution with options for:
- Verbose output (`-v`)
- Print statement display (`-s`)
- Custom test markers for environment-specific tests
- Test discovery patterns

## 🧪 Running Tests

### Run All Tests
```bash
python3 -m pytest
```

### Run Specific Test Files
```bash
# Company registration test
python3 -m pytest tests/test_register_company.py

# Bulk invitation test
python3 -m pytest tests/test_bulk_invite.py
```

### Run Tests with Specific Markers
```bash
# Development environment tests
python3 -m pytest -m dev

# Integration tests
python3 -m pytest -m integration

# Slow tests
python3 -m pytest -m slow
```

### Run Tests with Custom Options
```bash
# Run tests with maximum verbosity
python3 -m pytest -vvv

# Run tests and stop on first failure
python3 -m pytest -x

# Run tests in parallel (requires pytest-xdist)
python3 -m pytest -n auto
```

### Run Tests on Different Environments
```bash
# Development environment (default)
python3 -m pytest tests/test_register_company.py

# Staging environment
ENVIRONMENT=staging python3 -m pytest tests/test_register_company.py

# Test environment
ENVIRONMENT=test python3 -m pytest tests/test_register_company.py

# Production environment (use with caution)
ENVIRONMENT=prod python3 -m pytest tests/test_register_company.py
```

## 📋 Test Scenarios

### 1. Company Registration Test (`test_register_company.py`)

**Purpose:** End-to-end validation of the complete user onboarding process.

**Test Flow:**
1. User signup with email verification
2. Company details registration
3. User preferences survey
4. Dashboard access and admin UI validation
5. Profile information verification

**Usage:**
```bash
# Run with default environment (dev)
python3 -m pytest tests/test_register_company.py -v

# Run with specific environment
ENVIRONMENT=staging python3 -m pytest tests/test_register_company.py -v
ENVIRONMENT=test python3 -m pytest tests/test_register_company.py -v
```

### 2. Bulk Invitation Test (`test_bulk_invite.py`)

**Purpose:** Validation of bulk team member invitation functionality.

**Test Flow:**
1. User authentication with OTP verification
2. Navigation to team management section
3. Bulk invite interface access
4. CSV file upload and processing
5. Member invitation validation and role verification

**Usage:**
```bash
# Run with default environment (dev)
python3 -m pytest tests/test_bulk_invite.py -v

# Run with specific environment
ENVIRONMENT=staging python3 -m pytest tests/test_bulk_invite.py -v
ENVIRONMENT=test python3 -m pytest tests/test_bulk_invite.py -v
```

## 🏗️ Architecture

### Page Object Model (POM)

The framework implements the Page Object Model pattern for maintainable test code:

- **`pages/`** - Contains page object classes that encapsulate page interactions
- **Element Locators** - Centralized element selectors for easy maintenance
- **Business Logic** - Page-specific methods that represent user actions
- **Reusability** - Page objects can be shared across multiple test scenarios

### Utility Modules

- **`utils/api_utils.py`** - Handles API interactions for email verification
- **`utils/data_utils.py`** - Generates test data using Faker library
- **`config/environments.py`** - Manages environment-specific configurations

### Test Data Management

- **Dynamic Generation** - Uses Faker library for realistic test data
- **Unique Values** - Ensures each test run uses different data
- **Data Cleaning** - Sanitizes generated data for form compatibility

## 🔍 Test Data

### Default Test Values

```python
DEFAULT_FIRST_NAME = "Automation"
DEFAULT_LAST_NAME = "Tester"
DEFAULT_PASSWORD = "StrongPass123!"
```

### Generated Test Data

- **Company Names** - Realistic business names without special characters
- **Email Addresses** - Unique company emails for each test run
- **Contact Information** - Standardized test phone numbers

## 🚨 Important Notes

### OTP Handling

Tests use hardcoded OTP values ("5") for testing purposes. In production:
- Implement proper OTP retrieval from email/SMS
- Use secure token management
- Consider API-based verification bypass

### reCAPTCHA

The framework includes graceful reCAPTCHA handling:
- Attempts to complete reCAPTCHA verification
- Falls back gracefully if reCAPTCHA is not present
- Logs warnings for debugging purposes

### Timeouts

Tests include appropriate timeouts for:
- Page loading (20-30 seconds)
- API responses (10-60 seconds)
- Dynamic content rendering

## 🐛 Troubleshooting

### Common Issues

1. **Browser Launch Failures**
   - Ensure Playwright browsers are installed: `playwright install`
   - Check system dependencies for browser requirements

2. **Element Not Found Errors**
   - Verify element selectors are up-to-date
   - Check for dynamic content loading delays
   - Ensure proper wait conditions

3. **Test Data Issues**
   - Verify Faker library is properly installed
   - Check for unique constraint violations
   - Ensure data cleaning functions work correctly

### Debug Mode

Run tests with visible browser for debugging:
```python
# Tests are configured to run with visible browser by default
browser = p.chromium.launch(headless=False, args=["--start-maximized"])
```

### Screenshots

Tests automatically capture screenshots on completion:
```python
page.screenshot(path="company_pom.png")
```

## 📚 Additional Resources

### Documentation
- [Playwright Python Documentation](https://playwright.dev/python/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Faker Library Documentation](https://faker.readthedocs.io/)

### Best Practices
- [Page Object Model Pattern](https://www.selenium.dev/documentation/test_practices/encouraged/page_object_models/)
- [Test Automation Best Practices](https://martinfowler.com/articles/microservice-testing/)




