# API Utilities Module
# ====================
# This module provides utility functions for interacting with the Pemo application's
# REST API endpoints. It handles authentication flows, email verification,
# and URL construction for the test automation framework.

import requests
from config.environments import API_URL, HOME_URL

def resend_registration_email(email: str) -> str:
    """
    Trigger the resend registration email API endpoint and extract the verification token.
    
    This function is used in the user registration flow to:
    1. Request a new verification email for a given email address
    2. Extract the verification token from the API response
    3. Enable the test to proceed with email verification
    
    Args:
        email (str): The email address to resend the verification email to
        
    Returns:
        str: The verification token extracted from the API response
        
    Raises:
        AssertionError: If the API returns a non-200 status code
        
    Note:
        This endpoint is typically used when testing the complete user registration
        flow, as it allows bypassing the actual email delivery mechanism.
    """
    # Make POST request to the resend registration email endpoint
    response = requests.post(
        f"{API_URL}/identity/v1/auth/resend-registration-email",
        json={"email": email},
        headers={"Content-Type": "application/json"}
    )
    
    # Assert that the API call was successful
    # This ensures the test fails early if there are API issues
    assert response.status_code == 200, f"Unexpected status: {response.status_code}, {response.text}"
    
    # Extract and return the verification token from the response
    return response.json().get("token")

def build_redirect_url(token: str) -> str:
    """
    Build the redirect URL for email verification completion.
    
    This function constructs the URL that users are redirected to after
    clicking the verification link in their email. The token is appended
    as a hash fragment to maintain security.
    
    Args:
        token (str): The verification token received from the API
        
    Returns:
        str: The complete redirect URL with the verification token
        
    Example:
        Input: token="abc123"
        Output: "https://app.dev.pemo.io/email-verified/#abc123"
        
    Note:
        The token is appended as a hash fragment (#) rather than a query
        parameter to prevent it from being logged in server access logs.
    """
    return f"{HOME_URL}/email-verified/#{token}"





