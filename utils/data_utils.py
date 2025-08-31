# Data Utilities Module
# =====================
# This module provides utility functions for generating test data and managing
# default values used throughout the test automation framework.
# It uses the Faker library to generate realistic test data.

from faker import Faker
import re

# Initialize Faker instance for generating fake data
fake = Faker()

# Default Test User Configuration
# ==============================
# These constants define the default user credentials and personal information
# used across all test scenarios for consistency and maintainability
DEFAULT_FIRST_NAME = "Automation"  # Standard first name for test users
DEFAULT_LAST_NAME = "Tester"       # Standard last name for test users
DEFAULT_PASSWORD = "StrongPass123!" # Strong password meeting security requirements

def generate_test_email() -> str:
    """
    Generate a unique random company email for user signup testing.
    
    Returns:
        str: A unique fake company email address (e.g., "john.doe@acme-corp.com")
        
    Note:
        Uses Faker's unique company_email() method to ensure no duplicate emails
        are generated within the same test session.
    """
    return fake.unique.company_email()

def generate_company_name() -> str:
    """
    Generate a clean, valid company name suitable for form submission.
    
    This function takes a fake company name and sanitizes it by:
    1. Removing special characters that might cause form validation issues
    2. Keeping only letters, numbers, and spaces
    3. Normalizing multiple spaces into single spaces
    4. Trimming leading/trailing whitespace
    
    Returns:
        str: A clean company name without special characters
        
    Example:
        Input: "Johnson, Smith & Associates, Inc."
        Output: "Johnson Smith Associates Inc"
    """
    # Generate a fake company name using Faker
    name = fake.company()
    
    # Clean the company name by removing special characters
    # Keep only letters, numbers, and spaces for form compatibility
    clean_name = re.sub(r'[^A-Za-z0-9 ]+', '', name)
    
    # Normalize multiple consecutive spaces into single spaces
    # and remove leading/trailing whitespace
    clean_name = re.sub(r'\s+', ' ', clean_name).strip()
    
    return clean_name
