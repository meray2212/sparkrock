""" This is a draft of the bulk invite test. It is not used in the project. """

from playwright.sync_api import sync_playwright, Page, expect
import csv
import random
import string
import tempfile
import os
import time


def generate_random_emails(num_emails: int, file_path: str):
    """Generate random emails and save to CSV"""
    random_emails = []
    for _ in range(num_emails):
        name = ''.join(random.choices(string.ascii_lowercase, k=8))
        email = f"{name}@example.com"
        random_emails.append(email)

    # Write to CSV
    with open(file_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["emails"])  # header
        for email in random_emails:
            writer.writerow([email])

    return random_emails[0], random_emails[1]


def login_with_otp(page: Page, username: str, password: str):
    page.goto("https://app.dev.pemo.io/")

    page.wait_for_selector("text=Log in")
    page.fill("input[name='email']", username)
    page.fill("input[name='password']", password)
    page.click("xpath=//button[@id='login-btn']")

    page.wait_for_selector("button:has-text('Next')", timeout=60000)
    page.click("button:has-text('Next')")

    # OTP entry
    page.wait_for_selector("//input[contains(@class,'MuiOutlinedInput-input') and @type='text']", timeout=10000)
    otp_inputs = page.locator("//input[contains(@class,'MuiOutlinedInput-input') and @type='text']")
    count = otp_inputs.count()
    for i in range(count):
        input_box = otp_inputs.nth(i)
        input_box.click(force=True)
        page.keyboard.type("5")

    page.click("xpath=(//button[normalize-space()='Confirm'])[1]")
    page.wait_for_selector("text=Home", timeout=60000)


def search_and_assert_member(page: Page, email_to_search: str, role_to_assert: str):
    """Search for an invited member and validate role + invite status"""
    time.sleep(10)  # mimic Robot sleep
    page.reload()

    # Search box
    page.fill("//input[@id='members-search-input']", email_to_search)
    time.sleep(5)

    # Assert role
    page.wait_for_selector(
        "//p[contains(@class, 'MuiTypography-body1') and "
        "(text()='Team Member' or text()='Admin' or text()='Accountant')]",
        timeout=20000,
    )
    assert role_to_assert in page.inner_text(
        "//p[contains(@class, 'MuiTypography-body1') and "
        "(text()='Team Member' or text()='Admin' or text()='Accountant')]"
    )

    # Assert invite status
    page.wait_for_selector(
        "//span[contains(@class, 'MuiChip-label') and text()='Invite sent']",
        timeout=20000,
    )
    assert "Invite sent" in page.inner_text(
        "//span[contains(@class, 'MuiChip-label') and text()='Invite sent']"
    )
    time.sleep(2)


def test_bulk_invite_members():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=["--start-maximized"]
        )
        context = browser.new_context(no_viewport=True)
        page = context.new_page()

        # Login
        login_with_otp(page, "admin@autotest.io", "Admin@123")

        # Navigate to Members & Teams
        page.wait_for_selector("//span[text()='Members & Teams']", timeout=20000)
        page.click("//span[text()='Members & Teams']")

        page.wait_for_selector("//button[@id='invite-btn']", timeout=20000)
        page.click("//button[@id='invite-btn']")
        page.wait_for_selector("//button[@id='tab-bulk']")

        # Bulk invite tab
        page.click("//button[@id='tab-bulk']")

        # --- CSV upload flow ---
        # Step 1: Click upload area first
        page.wait_for_selector("//p[@title='Upload CSV file']", timeout=20000)
        page.click("//p[@title='Upload CSV file']")

        # Step 2: Create temp CSV
        tmp_dir = tempfile.gettempdir()
        csv_path = os.path.join(tmp_dir, "bulk_invite.csv")
        email_1, email_2 = generate_random_emails(2, csv_path)

        # Step 3: Upload CSV file
        page.set_input_files("input[type='file']", csv_path)

        # Submit
        page.click("button:has-text('Send invites')")
        

        # Search + assert the first invited email
        search_and_assert_member(page, email_1, "Team Member")
        search_and_assert_member(page, email_1, "Team Member")
        print("✅ Bulk invite + search assertion passed!")

        browser.close()


if __name__ == "__main__":
    test_bulk_invite_members()
