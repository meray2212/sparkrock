# Company Page Object Module
# ==========================
# This module implements the Page Object Model (POM) pattern for the company
# registration page of the Pemo application. It handles the business setup
# process after user registration, including company details and preferences.

from utils.data_utils import generate_company_name

class CompanyPage:
    """
    Page Object representing the company registration page of the Pemo application.
    
    This class provides methods to complete the business setup process after
    user registration. It handles:
    - Company information input (name, contact details)
    - Company size selection
    - Terms and conditions acceptance
    - Form submission to complete business registration
    
    The class uses utility functions to generate valid company data and
    implements the Page Object Model pattern for maintainable test code.
    
    Attributes:
        page: The Playwright page object for browser interaction
        company_name_input (str): CSS selector for company name input
        contact_number_input (str): CSS selector for contact number input
        checkbox (str): CSS selector for terms acceptance checkbox
        company_size_dropdown (str): XPath selector for company size dropdown
        company_size_option (str): XPath selector for specific company size option
        submit_button (str): CSS selector for form submission button
    """
    
    def __init__(self, page):
        """
        Initialize the CompanyPage with a Playwright page object.
        
        Args:
            page: The Playwright page object for browser automation
        """
        self.page = page

        # Page Element Locators
        # =====================
        # These selectors identify the key elements on the company registration page
        # They are grouped by functionality for better organization
        
        # Company Information Fields
        self.company_name_input = "input[name='name']"             # Company name input field
        self.contact_number_input = "input[name='contactNumber']"  # Contact phone number input
        
        # Form Controls and Validation
        self.checkbox = "input.PrivateSwitchBase-input[type='checkbox']"  # Terms acceptance checkbox
        
        # Company Size Selection
        self.company_size_dropdown = "(//div[@id='company-size'])[1]"     # Company size dropdown trigger
        self.company_size_option = "//p[normalize-space()='51 to 250 employees']"  # Specific size option
        
        # Form Submission
        self.submit_button = "button#register-business-submit-btn"        # Submit button to complete registration

    def fill_company_details(self):
        """
        Complete the company registration form with generated test data.
        
        This method performs the complete business setup process:
        1. Waits for the company form to load
        2. Generates a valid company name using utility functions
        3. Fills in company contact information
        4. Accepts terms and conditions
        5. Selects appropriate company size
        6. Submits the form to complete business registration
        
        Note:
            The method uses a hardcoded contact number for testing purposes.
            Company names are generated dynamically to ensure uniqueness.
            The checkbox is clicked using JavaScript to ensure reliable interaction.
            Company size is set to "51 to 250 employees" as a realistic test value.
        """
        # Wait for the company registration form to be fully loaded
        # Extended timeout (20s) accounts for potential page load delays
        self.page.wait_for_selector(self.company_name_input, timeout=20000)

        # Company Name Generation
        # =======================
        # Generate a unique, valid company name using the utility function
        # This ensures each test run uses a different company name
        company_name = generate_company_name()

        # Form Field Population
        # =====================
        # Fill in company name with the generated value
        self.page.fill(self.company_name_input, company_name)
        
        # Fill in contact number with a standard test phone number
        # This is hardcoded for consistency across test runs
        self.page.fill(self.contact_number_input, "98765321")

        # Terms and Conditions Acceptance
        # ==============================
        # Click the checkbox to accept terms and conditions
        # Using JavaScript click for reliability since normal clicks sometimes fail
        # This ensures the checkbox is properly checked before form submission
        self.page.click("input.PrivateSwitchBase-input[type='checkbox']")

        # Company Size Selection
        # =====================
        # Open the company size dropdown and select a specific option
        # This simulates a realistic company size selection
        self.page.click(self.company_size_dropdown)
        self.page.click(self.company_size_option)

        # Form Submission
        # ===============
        # Click the submit button to complete the company registration process
        # This will proceed to the next step in the onboarding flow
        self.page.click(self.submit_button)
