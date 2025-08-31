# Members Page Object Module
# ==========================
# This module implements the Page Object Model (POM) pattern for the members
# and teams management page of the Pemo application. It handles bulk user
# invitation processes including CSV file generation, upload, and validation.

import time
import os
import csv
import random
import string
import tempfile
from playwright.sync_api import Page

class MembersPage:
    """
    Page Object representing the members and teams management page of the Pemo application.
    
    This class provides methods to manage team members including:
    - Navigation to the members management section
    - Bulk invitation of users via CSV file upload
    - Generation of test CSV files with random email addresses
    - Validation of invited member status and roles
    - Search functionality for member verification
    
    The class implements the Page Object Model pattern and includes utilities
    for generating test data and managing temporary files.
    
    Attributes:
        page (Page): The Playwright page object for browser interaction
        members_teams_menu (str): XPath selector for members menu navigation
        invite_button (str): XPath selector for invite button
        bulk_tab_button (str): XPath selector for bulk invite tab
        upload_csv_title (str): XPath selector for CSV upload area
        file_input (str): CSS selector for file input element
        send_invites_button (str): CSS selector for send invites button
        search_input (str): XPath selector for member search input
        role_label (str): XPath selector for member role display
        invite_sent_chip (str): XPath selector for invite status indicator
    """
    
    def __init__(self, page: Page):
        """
        Initialize the MembersPage with a Playwright page object.
        
        Args:
            page (Page): The Playwright page object for browser automation
        """
        self.page = page

        # Page Element Locators
        # =====================
        # These selectors identify the key elements on the members page
        # They are grouped by functionality for better organization
        
        # Navigation and Menu Elements
        self.members_teams_menu = "//span[text()='Members & Teams']"  # Main navigation menu item
        
        # Bulk Invite Interface Elements
        self.invite_button = "//button[@id='invite-btn']"              # Invite button to open invite modal
        self.bulk_tab_button = "//button[@id='tab-bulk']"              # Bulk invite tab selection
        self.upload_csv_title = "//p[@title='Upload CSV file']"        # CSV upload area trigger
        self.file_input = "input[type='file']"                         # File input element for CSV upload
        self.send_invites_button = "button:has-text('Send invites')"   # Submit button for bulk invites
        
        # Member Management and Search Elements
        self.search_input = "//input[@id='members-search-input']"      # Member search input field
        self.role_label = (
            "//p[contains(@class, 'MuiTypography-body1') and "
            "(text()='Team Member' or text()='Admin' or text()='Accountant')]"
        )  # Member role display element
        self.invite_sent_chip = (
            "//span[contains(@class, 'MuiChip-label') and text()='Invite sent']"
        )  # Invite status indicator

    def navigate(self):
        """
        Navigate to the Members & Teams section of the application.
        
        This method waits for the members menu to be available and clicks
        it to access the team management functionality. It includes appropriate
        waits to ensure reliable navigation.
        
        Note:
            The method waits up to 20 seconds for the menu to be available,
            accounting for potential page load delays in the application.
        """
        # Wait for the Members & Teams menu item to be available
        # Extended timeout (20s) accounts for potential page load delays
        self.page.wait_for_selector(self.members_teams_menu, timeout=20000)
        
        # Click the menu item to navigate to the members section
        self.page.click(self.members_teams_menu)

    def open_bulk_invite(self):
        """
        Open the bulk invite interface for inviting multiple team members.
        
        This method performs the following steps:
        1. Waits for the invite button to be available
        2. Clicks the invite button to open the invite modal
        3. Switches to the bulk invite tab for CSV-based invitations
        
        Note:
            The method includes appropriate waits between actions to ensure
            reliable interaction with the dynamic interface elements.
        """
        # Wait for the invite button to be available and click it
        # Extended timeout (20s) accounts for potential page load delays
        self.page.wait_for_selector(self.invite_button, timeout=20000)
        self.page.click(self.invite_button)

        # Wait for the bulk invite tab to be available and click it
        # This switches the interface to CSV-based bulk invitation mode
        self.page.wait_for_selector(self.bulk_tab_button, timeout=20000)
        self.page.click(self.bulk_tab_button)

    def generate_random_emails(self, num_emails: int, file_path: str):
        """
        Generate random email addresses and save them to a CSV file for bulk invitation.
        
        This method creates test data for bulk invitation testing:
        1. Generates the specified number of random email addresses
        2. Creates a CSV file with the proper header structure
        3. Writes the email addresses to the CSV file
        4. Returns the first two emails for validation purposes
        
        Args:
            num_emails (int): The number of random email addresses to generate
            file_path (str): The file path where the CSV should be saved
            
        Returns:
            tuple: A tuple containing the first two generated email addresses
                   (email_1, email_2) for validation purposes
                   
        Note:
            The method generates realistic-looking email addresses using random
            lowercase letters. The CSV format matches the application's expected
            structure with an "emails" header column.
        """
        # Generate random email addresses for testing
        random_emails = []
        for _ in range(num_emails):
            # Create a random 8-character name using lowercase letters
            name = ''.join(random.choices(string.ascii_lowercase, k=8))
            # Construct email address using the random name
            email = f"{name}@example.com"
            random_emails.append(email)

        # Write the generated emails to a CSV file
        # The file structure matches the application's expected format
        with open(file_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["emails"])  # CSV header column
            for email in random_emails:
                writer.writerow([email])

        # Return the first two emails for validation purposes
        # This allows tests to verify the invitation process
        return random_emails[0], random_emails[1]

    def upload_bulk_csv(self):
        """
        Upload a CSV file containing email addresses for bulk invitation.
        
        This method performs the complete bulk invitation process:
        1. Waits for the CSV upload interface to be ready
        2. Generates a temporary CSV file with test email addresses
        3. Uploads the CSV file to the application
        4. Submits the bulk invitation request
        5. Returns the generated email addresses for validation
        
        Returns:
            tuple: A tuple containing the first two generated email addresses
                   (email_1, email_2) for validation purposes
                   
        Note:
            The method creates a temporary CSV file in the system's temp directory
            and generates 2 test email addresses. The file is automatically
            cleaned up by the system after the test completes.
        """
        # Wait for the CSV upload interface to be ready
        # Extended timeout (20s) accounts for potential interface loading delays
        self.page.wait_for_selector(self.upload_csv_title, timeout=20000)
        self.page.click(self.upload_csv_title)

        # Create a temporary CSV file with test email addresses
        # Use the system's temporary directory for proper cleanup
        tmp_dir = tempfile.gettempdir()
        csv_path = os.path.join(tmp_dir, "bulk_invite.csv")
        
        # Generate 2 test email addresses and save them to the CSV file
        email_1, email_2 = self.generate_random_emails(2, csv_path)

        # Upload the generated CSV file to the application
        self.page.set_input_files(self.file_input, csv_path)
        
        # Submit the bulk invitation request
        self.page.click(self.send_invites_button)

        # Return the generated email addresses for validation purposes
        return email_1, email_2

    def search_and_assert_member(self, email_to_search: str, role_to_assert: str):
        """
        Search for a specific member and validate their role and invitation status.
        
        This method performs comprehensive validation of the invitation process:
        1. Waits for the invitation processing to complete
        2. Reloads the page to ensure fresh data
        3. Searches for the specific email address
        4. Validates the member's assigned role
        5. Confirms the invitation status is "Invite sent"
        
        Args:
            email_to_search (str): The email address to search for
            role_to_assert (str): The expected role for the member
                                 (e.g., "Team Member", "Admin", "Accountant")
                                 
        Note:
            The method includes appropriate waits and timeouts to ensure
            reliable validation. It uses assertions to verify both role
            and invitation status, ensuring the complete invitation flow
            was successful.
        """
        # Wait for invitation processing to complete
        # 10-second wait accounts for backend processing time
        time.sleep(10)
        
        # Reload the page to ensure fresh data is displayed
        # This is necessary to see the newly invited members
        self.page.reload()

        # Search for the specific email address
        self.page.fill(self.search_input, email_to_search)
        
        # Wait for search results to load
        # 5-second wait accounts for search processing time
        time.sleep(5)

        # Validate the member's assigned role
        # Wait for the role label to be visible and verify the expected role
        self.page.wait_for_selector(self.role_label, timeout=20000)
        assert role_to_assert in self.page.inner_text(self.role_label)

        # Confirm the invitation status is "Invite sent"
        # Wait for the status chip to be visible and verify the status
        self.page.wait_for_selector(self.invite_sent_chip, timeout=20000)
        assert "Invite sent" in self.page.inner_text(self.invite_sent_chip)

        # Brief wait to ensure all UI updates are complete
        time.sleep(2)
