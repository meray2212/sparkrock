# Signup Page Object Module
# =========================
# This module implements the Page Object Model (POM) pattern for the user signup page
# of the Pemo application. It handles the complete user registration flow including
# form filling, reCAPTCHA handling, and form submission.

from utils.data_utils import DEFAULT_FIRST_NAME, DEFAULT_LAST_NAME, DEFAULT_PASSWORD

class SignupPage:
    """
    Page Object representing the user signup/registration page of the Pemo application.
    
    This class provides methods to complete the user registration process including:
    - Filling out the signup form with user details
    - Handling reCAPTCHA verification (with fallback for testing)
    - Selecting user preferences and source information
    - Submitting the registration form
    
    The class uses default test data from data_utils for consistent testing
    and implements the Page Object Model pattern for maintainable test code.
    
    Attributes:
        page: The Playwright page object for browser interaction
        recaptcha_iframe (str): Selector for reCAPTCHA iframe
        recaptcha_anchor (str): Selector for reCAPTCHA checkbox
        email_input (str): XPath selector for email input field
        first_name_input (str): CSS selector for first name input
        last_name_input (str): CSS selector for last name input
        password_input (str): CSS selector for password input
        repeat_password_input (str): CSS selector for password confirmation
        source_combobox (str): XPath selector for source selection dropdown
        source_social_media (str): XPath selector for social media option
        get_started_button (str): CSS selector for form submission button
    """
    
    def __init__(self, page):
        """
        Initialize the SignupPage with a Playwright page object.
        
        Args:
            page: The Playwright page object for browser automation
        """
        self.page = page

        # Page Element Locators
        # =====================
        # These selectors identify the key elements on the signup page
        # They are grouped by functionality for better organization
        
        # reCAPTCHA Elements
        self.recaptcha_iframe = "iframe[title='reCAPTCHA']"        # reCAPTCHA iframe container
        self.recaptcha_anchor = "#recaptcha-anchor"                 # reCAPTCHA checkbox element
        
        # User Information Form Fields
        self.email_input = "xpath=(//input[@id='signUp-1-1'])[1]"  # Email address input
        self.first_name_input = "input[name='firstName']"           # First name input field
        self.last_name_input = "input[name='lastName']"             # Last name input field
        self.password_input = "input[name='password']"              # Password input field
        self.repeat_password_input = "input[name='repeatPassword']" # Password confirmation field
        
        # User Source Selection
        self.source_combobox = "//div[contains(@class, 'MuiSelect-outlined') and @role='combobox']"  # Source dropdown
        self.source_social_media = "//li[normalize-space()='Social Media']"                         # Social media option
        
        # Form Submission
        self.get_started_button = "button#get-started-submit-btn"   # Submit button to complete registration

    def fill_signup_form(self, email: str):
        """
        Complete the entire signup form with provided email and default test data.
        
        This method performs the complete user registration process:
        1. Attempts to handle reCAPTCHA verification (with graceful fallback)
        2. Fills in all required form fields with appropriate data
        3. Selects user source preference
        4. Submits the registration form
        
        Args:
            email (str): The email address to use for registration
                        This should be a unique email for each test run
                        
        Note:
            The method uses default test data for first name, last name, and password
            to ensure consistency across test runs. The reCAPTCHA handling includes
            a try-catch block to gracefully handle cases where reCAPTCHA is not
            present or cannot be interacted with during testing.
        """
        # reCAPTCHA Handling
        # ===================
        # Attempt to handle reCAPTCHA verification if present
        # This is wrapped in a try-catch to handle cases where reCAPTCHA
        # is not present or cannot be interacted with during testing
        try:
            # Locate the reCAPTCHA iframe and click the checkbox
            frame = self.page.frame_locator(self.recaptcha_iframe)
            frame.locator(self.recaptcha_anchor).click(timeout=5000)
            
            # Wait briefly for reCAPTCHA verification to complete
            self.page.wait_for_timeout(1000)
        except Exception:
            # Log warning and continue if reCAPTCHA cannot be handled
            # This allows tests to proceed even if reCAPTCHA is not present
            print("⚠️ reCAPTCHA skipped")

        # Form Field Population
        # =====================
        # Fill in all required form fields with appropriate test data
        self.page.fill(self.email_input, email)                    # User-provided email
        self.page.fill(self.first_name_input, DEFAULT_FIRST_NAME)  # Default first name
        self.page.fill(self.last_name_input, DEFAULT_LAST_NAME)    # Default last name
        self.page.fill(self.password_input, DEFAULT_PASSWORD)      # Default strong password
        self.page.fill(self.repeat_password_input, DEFAULT_PASSWORD)  # Password confirmation

        # User Source Selection
        # =====================
        # Open the source dropdown and select "Social Media" as the user source
        # This simulates how users typically discover the application
        self.page.locator(self.source_combobox).click()
        self.page.locator(self.source_social_media).click()

        # Form Submission
        # ===============
        # Click the submit button to complete the registration process
        # This will trigger the email verification flow
        self.page.click(self.get_started_button)
