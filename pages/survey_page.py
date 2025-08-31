# Survey Page Object Module
# =========================
# This module implements the Page Object Model (POM) pattern for the user
# survey/preferences page of the Pemo application. It handles the final
# step of user onboarding where users select their team and role preferences.

class SurveyPage:
    """
    Page Object representing the user survey/preferences page of the Pemo application.
    
    This class provides methods to complete the final user onboarding step:
    - Team selection from available options
    - Role selection within the chosen team
    - Saving preferences and proceeding to the main dashboard
    
    The survey page is typically shown after company registration and helps
    customize the user experience based on their role and team context.
    
    Attributes:
        page: The Playwright page object for browser interaction
        team_dropdown (str): XPath selector for team selection dropdown
        team_option_engineering (str): XPath selector for Engineering/IT team option
        role_dropdown (str): XPath selector for role selection dropdown
        role_option_manager (str): XPath selector for Manager role option
        save_button (str): XPath selector for save preferences button
        get_started_text (str): Text selector indicating successful completion
    """
    
    def __init__(self, page):
        """
        Initialize the SurveyPage with a Playwright page object.
        
        Args:
            page: The Playwright page object for browser automation
        """
        self.page = page

        # Page Element Locators
        # =====================
        # These selectors identify the key elements on the survey page
        # They are grouped by functionality for better organization
        
        # Team Selection Elements
        self.team_dropdown = "//label[contains(text(), 'Select a team')]/following-sibling::div//div[@role='combobox']"  # Team dropdown trigger
        self.team_option_engineering = "//li[@role='option' and @data-value='Engineering / IT']"                           # Engineering team option
        
        # Role Selection Elements
        self.role_dropdown = "//label[contains(text(), 'Select a role')]/following-sibling::div//div[@role='combobox']"  # Role dropdown trigger
        self.role_option_manager = "//li[text()='Manager']"                                                              # Manager role option
        
        # Form Completion Elements
        self.save_button = "(//button[normalize-space()='Save'])[1]"                                                      # Save preferences button
        self.get_started_text = "text=Get started"                                                                       # Success indicator text

    def fill_survey(self):
        """
        Complete the user survey by selecting team and role preferences.
        
        This method performs the complete survey completion process:
        1. Opens the team selection dropdown and selects "Engineering / IT"
        2. Opens the role selection dropdown and selects "Manager"
        3. Saves the preferences and waits for successful completion
        4. Verifies transition to the main dashboard
        
        Note:
            The method uses hardcoded selections for testing purposes:
            - Team: Engineering / IT (common in tech companies)
            - Role: Manager (mid-level management position)
            
            These selections are realistic and commonly used in test scenarios.
            The method includes appropriate waits to ensure reliable form interaction.
        """
        # Team Selection
        # ===============
        # Open the team dropdown and select the Engineering/IT option
        # This simulates a user choosing their primary team
        self.page.click(self.team_dropdown)
        self.page.click(self.team_option_engineering)

        # Role Selection
        # ===============
        # Open the role dropdown and select the Manager option
        # This simulates a user defining their position within the team
        self.page.click(self.role_dropdown)
        self.page.click(self.role_option_manager)

        # Save Preferences and Complete Onboarding
        # =======================================
        # Click the save button to submit the survey preferences
        # This completes the user onboarding process
        self.page.click(self.save_button)
        
        # Wait for the "Get started" text to appear, indicating successful
        # survey completion and transition to the main dashboard
        # Extended timeout (20s) accounts for potential processing delays
        self.page.wait_for_selector(self.get_started_text, timeout=20000)
