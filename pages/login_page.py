# Login Page Object Module
# ========================
# This module implements the Page Object Model (POM) pattern for the login page
# of the Pemo application. It encapsulates all login-related functionality
# including email/password authentication and OTP verification.

from playwright.sync_api import Page
from config.environments import HOME_URL

class LoginPage:
    """
    Page Object representing the login page of the Pemo application.
    
    This class provides methods to interact with the login form, handle
    OTP verification, and complete the authentication process. It uses
    Playwright for browser automation and implements the Page Object
    Model pattern for maintainable test code.
    
    Attributes:
        page (Page): The Playwright page object for browser interaction
        email_input (str): CSS selector for the email input field
        password_input (str): CSS selector for the password input field
        login_button (str): XPath selector for the login submit button
        next_button (str): CSS selector for the next button in OTP flow
        otp_inputs (str): XPath selector for OTP input fields
        confirm_button (str): XPath selector for the OTP confirmation button
        home_text (str): Text selector for the home page indicator
    """
    
    def __init__(self, page: Page):
        """
        Initialize the LoginPage with a Playwright page object.
        
        Args:
            page (Page): The Playwright page object for browser automation
        """
        self.page = page

        # Page Element Locators
        # =====================
        # These selectors identify the key elements on the login page
        # They are grouped by functionality for better organization
        
        # Authentication Form Elements
        self.email_input = "input[name='email']"                    # Email input field
        self.password_input = "input[name='password']"              # Password input field
        self.login_button = "xpath=//button[@id='login-btn']"      # Login submit button
        
        # OTP Verification Elements
        self.next_button = "button:has-text('Next')"               # Next button to proceed to OTP
        self.otp_inputs = "//input[contains(@class,'MuiOutlinedInput-input') and @type='text']"  # OTP input fields
        self.confirm_button = "xpath=(//button[normalize-space()='Confirm'])[1]"  # OTP confirmation button
        
        # Success Indicators
        self.home_text = "text=Home"                               # Text indicating successful login

    def login_with_otp(self, username: str, password: str):
        """
        Complete the full login process including OTP verification.
        
        This method performs a complete login flow:
        1. Navigate to the login page
        2. Fill in email and password credentials
        3. Submit the login form
        4. Handle OTP verification by entering a default code
        5. Wait for successful authentication and redirect to home
        
        Args:
            username (str): The user's email address
            password (str): The user's password
            
        Note:
            This method uses a hardcoded OTP value ("5") for testing purposes.
            In a real scenario, the OTP would be retrieved from email/SMS.
            The method includes appropriate waits and timeouts for reliable execution.
        """
        # Navigate to the login page
        # Use the imported HOME_URL variable from config
        self.page.goto(HOME_URL)

        # Wait for the login form to be visible and fill credentials
        self.page.wait_for_selector("text=Log in")
        self.page.fill(self.email_input, username)
        self.page.fill(self.password_input, password)
        self.page.click(self.login_button)

        # Wait for OTP flow to begin and proceed to next step
        # Extended timeout (60s) accounts for potential email delivery delays
        self.page.wait_for_selector(self.next_button, timeout=60000)
        self.page.click(self.next_button)

        # OTP Entry and Verification
        # ==========================
        # Wait for OTP input fields to appear (10s timeout)
        self.page.wait_for_selector(self.otp_inputs, timeout=10000)
        otp_inputs = self.page.locator(self.otp_inputs)
        
        # Fill all OTP input fields with the default test value "5"
        # This simulates entering a 6-digit OTP code
        for i in range(otp_inputs.count()):
            input_box = otp_inputs.nth(i)
            input_box.click(force=True)  # Force click to ensure focus
            self.page.keyboard.type("5")  # Enter default OTP digit

        # Submit the OTP verification
        self.page.click(self.confirm_button)
        
        # Wait for successful authentication and redirect to home page
        # Extended timeout (60s) accounts for potential processing delays
        self.page.wait_for_selector(self.home_text, timeout=60000)
