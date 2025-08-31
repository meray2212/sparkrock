# Dashboard Page Object Module
# ============================
# This module implements the Page Object Model (POM) pattern for the main
# dashboard page of the Pemo application. It provides methods to verify
# the admin user interface and validate that all expected elements are present.

class DashboardPage:
    """
    Page Object representing the main dashboard page of the Pemo application.
    
    This class provides methods to verify the admin user interface after
    successful login and onboarding. It validates the presence of:
    - Main navigation elements and menu items
    - Financial management features (cards, expenses, transactions)
    - Administrative tools (members, teams, policies)
    - User profile and account settings
    
    The dashboard serves as the central hub for all application functionality
    and this class ensures all expected elements are properly displayed.
    
    Attributes:
        page: The Playwright page object for browser interaction
        get_started_text (str): Text selector for onboarding completion indicator
        home_text (str): Text selector for home navigation element
        card_expenses_text (str): Text selector for card expenses feature
        cards_text (str): Text selector for cards management feature
        requests_text (str): Text selector for requests feature
        transactions_text (str): Text selector for transactions feature
        statements_text (str): Text selector for statements feature
        accounting_export_text (str): Text selector for accounting export feature
        members_teams_text (str): Text selector for members and teams feature
        more_button (str): XPath selector for more menu button
        invoices_text (str): Text selector for invoices feature
        reimbursements_text (str): Text selector for reimbursements feature
        budgets_text (str): Text selector for budgets feature
        approval_policies_text (str): Text selector for approval policies feature
        submission_policies_text (str): Text selector for submission policies feature
        receipts_inbox_text (str): Text selector for receipts inbox feature
        settings_button (str): XPath selector for settings menu button
        billing_text (str): Text selector for billing feature
        subscription_plans_text (str): Text selector for subscription plans feature
        user_full_name (str): XPath selector for user profile name display
        my_account_text (str): Text selector for my account option
        email_notifications_text (str): Text selector for email notifications option
        logout_text (str): Text selector for logout option
    """
    
    def __init__(self, page):
        """
        Initialize the DashboardPage with a Playwright page object.
        
        Args:
            page: The Playwright page object for browser automation
        """
        self.page = page

        # Page Element Locators
        # =====================
        # These selectors identify the key elements on the dashboard page
        # They are grouped by functionality for better organization
        
        # Main Navigation and Core Features
        self.get_started_text = "text=Get started"                 # Onboarding completion indicator
        self.home_text = "text=Home"                               # Home navigation element
        self.card_expenses_text = "text=Card expenses"             # Card expenses management
        self.cards_text = "text=Cards"                             # Cards management feature
        self.requests_text = "text=Requests"                       # Requests management
        self.transactions_text = "text=Transactions"               # Transaction history
        self.statements_text = "text=Statements"                   # Financial statements
        self.accounting_export_text = "text=Accounting export"     # Accounting data export
        self.members_teams_text = "text=Members & Teams"           # Team management

        # Extended Features (More Menu)
        self.more_button = "//span[normalize-space()='More']"      # More features menu button
        self.invoices_text = "text=Invoices"                       # Invoice management
        self.reimbursements_text = "text=Reimbursements"           # Reimbursement processing
        self.budgets_text = "text=Budgets"                         # Budget management
        self.approval_policies_text = "text=Approval policies"     # Approval workflow policies
        self.submission_policies_text = "text=Submission policies" # Submission guidelines
        self.receipts_inbox_text = "text=Receipts inbox"           # Receipt processing

        # Settings and Configuration
        self.settings_button = "//span[normalize-space()='Settings']"  # Settings menu button
        self.billing_text = "text=Billing"                             # Billing management
        self.subscription_plans_text = "text=Subscription plans"       # Plan management

        # User Profile and Account
        self.user_full_name = "xpath=//span[@id='user-full-name']"    # User's full name display
        self.my_account_text = "text=My account"                       # Account settings
        self.email_notifications_text = "text=Email notifications"     # Notification preferences
        self.logout_text = "text=Logout"                               # Logout option

    def verify_admin_ui(self, expected_user_name: str):
        """
        Verify that all expected admin user interface elements are present and visible.
        
        This method performs comprehensive validation of the dashboard interface:
        1. Verifies main navigation and core financial features
        2. Checks extended features available in the More menu
        3. Validates settings and configuration options
        4. Confirms user profile and account management features
        5. Validates the displayed user name matches expectations
        
        Args:
            expected_user_name (str): The expected user name to verify in the interface
                                     This should match the user who completed onboarding
                                     
        Note:
            The method uses assertions to ensure all expected elements are visible.
            It includes appropriate waits for dynamic content loading.
            The verification covers the complete admin user experience.
        """
        # Main Dashboard Interface Verification
        # ====================================
        # Wait for the onboarding completion indicator and verify core features
        # Extended timeout (30s) accounts for potential page load delays
        self.page.wait_for_selector(self.get_started_text, timeout=30000)
        
        # Verify all main navigation elements and core features are visible
        # These represent the primary functionality available to admin users
        assert self.page.is_visible(self.home_text)
        assert self.page.is_visible(self.card_expenses_text)
        assert self.page.is_visible(self.cards_text)
        assert self.page.is_visible(self.requests_text)
        assert self.page.is_visible(self.transactions_text)
        assert self.page.is_visible(self.statements_text)
        assert self.page.is_visible(self.accounting_export_text)
        assert self.page.is_visible(self.members_teams_text)

        # Extended Features Verification (More Menu)
        # =========================================
        # Open the More menu to access additional features
        self.page.click(self.more_button)
        
        # Verify all extended features are available and visible
        # These provide additional administrative and financial management capabilities
        assert self.page.is_visible(self.invoices_text)
        assert self.page.is_visible(self.reimbursements_text)
        assert self.page.is_visible(self.budgets_text)
        assert self.page.is_visible(self.approval_policies_text)
        assert self.page.is_visible(self.submission_policies_text)
        assert self.page.is_visible(self.receipts_inbox_text)

        # Settings and Configuration Verification
        # =====================================
        # Open the Settings menu to access configuration options
        self.page.click(self.settings_button)
        
        # Verify all settings and configuration features are available
        # These allow users to manage billing and subscription preferences
        assert self.page.is_visible(self.billing_text)
        assert self.page.is_visible(self.subscription_plans_text)

        # User Profile and Account Verification
        # ====================================
        # Open the user profile menu to access account management options
        self.page.click(self.user_full_name)
        
        # Verify all user account management features are available
        # These provide users with control over their account settings
        assert self.page.is_visible(self.my_account_text)
        assert self.page.is_visible(self.email_notifications_text)
        assert self.page.is_visible(self.logout_text)

        # User Name Validation
        # ====================
        # Extract the displayed user name and verify it matches expectations
        # This ensures the correct user account is active
        user_name = self.page.inner_text(self.user_full_name)
        assert expected_user_name in user_name
