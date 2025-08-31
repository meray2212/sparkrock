# Bulk Invite Test Module
# ========================
# This module contains the test for bulk invitation functionality in the
# Pemo application. It tests the process of inviting multiple team
# members simultaneously using CSV file upload.
#
# Test Flow:
# 1. User login with OTP verification
# 2. Navigate to members management section
# 3. Open bulk invite interface
# 4. Upload CSV with test email addresses
# 5. Validate invitation success and member status

from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from pages.members_page import MembersPage


def test_bulk_invite_members():
    """
    Test for bulk invitation of multiple team members via CSV upload.
    
    This test validates the bulk invitation functionality including:
    - User authentication and login
    - Navigation to team management section
    - Bulk invite interface access
    - CSV file upload and processing
    - Member invitation validation
    - Role assignment verification
    
    The test uses the Page Object Model pattern and generates
    random test email addresses for each execution.
    
    Test Steps:
    1. Authenticate user with OTP verification
    2. Navigate to Members & Teams section
    3. Open bulk invite interface and switch to CSV tab
    4. Generate and upload CSV file with test emails
    5. Validate that invited members appear with correct roles
    6. Verify invitation status for each member
    
    Note:
        This test requires valid admin credentials and assumes the
        user has permissions to invite team members. It generates
        temporary CSV files that are automatically cleaned up.
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

        # Test Step 1: User Authentication
        # =================================
        # Initialize login page object and complete authentication
        # This includes email/password entry and OTP verification
        login = LoginPage(page)
        login.login_with_otp("admin@autotest.io", "Admin@123")

        # Test Step 2: Navigate to Members Management
        # ===========================================
        # Initialize members page object and navigate to team management
        # This provides access to member invitation and management features
        members = MembersPage(page)
        members.navigate()
        
        # Open the bulk invite interface and switch to CSV upload mode
        # This enables inviting multiple users simultaneously
        members.open_bulk_invite()
        
        # Test Step 3: Process Bulk Invitations
        # =====================================
        # Upload CSV file with test email addresses and send invitations
        # This generates 2 random test emails and processes the bulk invite
        email_1, email_2 = members.upload_bulk_csv()

        # Test Step 4: Validate Invitation Results
        # =======================================
        # Search for each invited member and verify their status
        # This validates both the invitation process and role assignment
        
        # Validate first invited member
        # Verify they appear with "Team Member" role and "Invite sent" status
        members.search_and_assert_member(email_1, "Team Member")
        
        # Validate second invited member
        # Verify they also appear with "Team Member" role and "Invite sent" status
        members.search_and_assert_member(email_2, "Team Member")
        
        # Print success message to indicate test completion
        print("✅ Bulk invite + search assertion passed!")

        # Clean up browser resources
        browser.close()
