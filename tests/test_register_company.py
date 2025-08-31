# Company Registration Test Module
# =================================
# This module contains the main end-to-end test for the complete company
# registration flow in the Pemo application. It tests the entire user
# onboarding process from signup to dashboard access.
#
# Test Flow:
# 1. User signup with email verification
# 2. Company details registration
# 3. User preferences survey
# 4. Dashboard access and admin UI validation
# 5. Profile verification

from playwright.sync_api import sync_playwright
from utils.data_utils import (
    DEFAULT_FIRST_NAME,
    DEFAULT_LAST_NAME,
    generate_test_email
)
from utils.api_utils import resend_registration_email, build_redirect_url

from pages.signup_page import SignupPage
from pages.company_page import CompanyPage
from pages.survey_page import SurveyPage
from pages.dashboard_page import DashboardPage
from config.environments import  HOME_URL , API_URL


def test_register_company_uae():
    """
    End-to-end test for complete company registration and user onboarding.
    
    This test validates the entire user registration flow including:
    - User signup with email verification
    - Company information registration
    - User preferences and team/role selection
    - Dashboard access and admin interface validation
    - Profile information verification
    
    The test uses the Page Object Model pattern for maintainable code
    and generates unique test data for each execution.
    
    Test Steps:
    1. Open signup page and navigate to registration form
    2. Fill signup form with generated email and default user data
    3. Trigger email verification via API and redirect to verification page
    4. Complete company registration with generated business details
    5. Fill user survey with team and role preferences
    6. Verify admin dashboard interface and functionality
    7. Validate user profile information matches registration data
    
    Note:
        This test requires a working email verification system or API access
        to bypass the actual email delivery mechanism. It uses hardcoded
        OTP values and default test data for consistent execution.
    """
    # Initialize Playwright browser automation
    with sync_playwright() as p:
        # Launch Chromium browser in visible mode for debugging
        # Start maximized to ensure consistent element visibility
        browser = p.chromium.launch(headless=False, args=["--start-maximized"])
        
        # Create new browser context without viewport restrictions
        # This ensures the browser window uses full screen dimensions
        context = browser.new_context(no_viewport=True)
        
        # Create new page for test execution
        page = context.new_page()

        # Test Step 1: Open Signup Page
        # ===============================
        # Navigate to the main application URL
        page.goto(HOME_URL)
        
        # Wait for signup button to be available and click it
        # Extended timeout (20s) accounts for potential page load delays
        page.wait_for_selector("button#signup-btn", timeout=20000).click()
        
        # Wait for the signup form to load and display "Get Started" text
        # This confirms successful navigation to the registration page
        page.wait_for_selector("text=Get Started", timeout=10000)

        # Test Step 2: Fill Signup Form
        # ===============================
        # Generate unique company email for this test run
        # This ensures each test execution uses different data
        company_signup_email = generate_test_email()
        print("Signup Email:", company_signup_email)
        
        # Initialize signup page object and complete the registration form
        # The form includes user details, password, and source selection
        signup = SignupPage(page)
        signup.fill_signup_form(company_signup_email)

        # Test Step 3: Email Verification and Redirect
        # ============================================
        # Trigger the resend registration email API to get verification token
        # This bypasses the actual email delivery for testing purposes
        token = resend_registration_email(company_signup_email)
        
        # Build the redirect URL for email verification completion
        # The token is appended as a hash fragment for security
        redirect_url = build_redirect_url(token)
        
        # Navigate to the verification completion page
        # This simulates clicking the verification link in the email
        page.goto(redirect_url)

        # Test Step 4: Complete Company Registration
        # ==========================================
        # Initialize company page object and fill company details
        # This includes company name, contact information, and size selection
        company_page = CompanyPage(page)
        company_page.fill_company_details()

        # Test Step 5: Complete User Survey
        # =================================
        # Initialize survey page object and fill user preferences
        # This includes team selection and role assignment
        survey = SurveyPage(page)
        survey.fill_survey()

        # Test Step 6: Verify Admin Dashboard Interface
        # ============================================
        # Initialize dashboard page object and validate admin UI
        # This verifies all expected features and navigation elements
        admin = DashboardPage(page)
        admin.verify_admin_ui(expected_user_name=f"{DEFAULT_FIRST_NAME} {DEFAULT_LAST_NAME}")

        # Test Step 7: Verify User Profile Information
        # ============================================
        # Navigate to user account settings to verify profile data
        page.click("//span[contains(text(),'My account')]")
        
        # Wait for email input field to be available and extract its value
        # Extended timeout (30s) accounts for potential page load delays
        page.wait_for_selector("//input[@id='email-input']", timeout=30000)
        element_text = page.get_attribute("//input[@id='email-input']", "value")
        
        # Assert that the displayed email matches the registration email
        # This validates that user data was properly stored and retrieved
        assert element_text == company_signup_email, "Email mismatch"

        # Capture screenshot for test documentation and debugging
        # This provides visual evidence of successful test completion
        page.screenshot(path="company_pom.png")
        
        # Clean up browser resources
        browser.close()
