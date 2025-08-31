""" This is a draft of the company signup  test. It is not used in the project. """

from playwright.sync_api import sync_playwright
from faker import Faker
import requests
import time
import json

fake = Faker()

BASE_URL = "https://app.dev.pemo.io"
API_BASE_URL = "https://api.dev.pemo.io"  # adjust if API differs
DEFAULT_FIRST_NAME = "Automation"
DEFAULT_LAST_NAME = "Tester"
DEFAULT_PASSWORD = "StrongPass123!"


def test_register_company_uae():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            args=["--start-maximized"]
        )
        context = browser.new_context(no_viewport=True)
        page = context.new_page()

        # === Step 1: Open signup page ===
        page.goto(BASE_URL)
        page.wait_for_selector("button#signup-btn", timeout=20000).click()
        page.wait_for_selector("text=Get Started", timeout=10000)

        # === Step 2: Generate email and fill registration form ===
        company_signup_email = fake.company_email()
        print("Signup Email:", company_signup_email)

        fill_registration_form(page, company_signup_email)

        # === Step 3: Resend email & build redirect URL ===
        token = resend_registration_email(company_signup_email)
        redirect_url = build_redirect_url(token)
        print("Redirect URL:", redirect_url)
        page.goto(redirect_url)

        # === Step 4: Fill company details ===
        fill_company_details(page)

        # === Step 5: Fill survey ===
        fill_survey(page)

        # === Step 6: Admin UI checks ===
        admin_pages_check(page, expected_user_name=f"{DEFAULT_FIRST_NAME} {DEFAULT_LAST_NAME}")

        # === Verify stored email in profile ===
        page.click("//span[contains(text(),'My account')]")
        page.wait_for_selector("//input[@id='email-input']", timeout=30000)
        element_text = page.get_attribute("//input[@id='email-input']", "value")
        assert element_text == company_signup_email, "Email mismatch"

        page.screenshot(path="company_.png")
        browser.close()


def fill_registration_form(page, email):
    """Fill signup form"""
    # Handle reCAPTCHA iframe (if present)
    try:
        frame = page.frame_locator("iframe[title='reCAPTCHA']")
        frame.locator("#recaptcha-anchor").click(timeout=10000)
        page.wait_for_timeout(2000)
    except Exception:
        print("⚠️ reCAPTCHA not found / skipped")

    # Fill form
    page.fill("xpath=(//input[@id='signUp-1-1'])[1]", email)
    page.fill("input[name='firstName']", DEFAULT_FIRST_NAME)
    page.fill("input[name='lastName']", DEFAULT_LAST_NAME)
    page.fill("input[name='password']", DEFAULT_PASSWORD)
    page.fill("input[name='repeatPassword']", DEFAULT_PASSWORD)

    # Select dropdown
    page.locator("//div[contains(@class, 'MuiSelect-outlined') and @role='combobox']").click()
    page.locator("//li[normalize-space()='Social Media']").click()

    page.wait_for_timeout(2000)
    page.click("button#get-started-submit-btn")


def resend_registration_email(email):
    """Trigger resend email API & extract token"""
    body = {"email": email}
    headers = {"Content-Type": "application/json"}
    response = requests.post(f"{API_BASE_URL}/identity/v1/auth/resend-registration-email",
                             json=body, headers=headers)
    print("Resend Email Status:", response.status_code)
    assert response.status_code == 200
    data = response.json()
    return data.get("token", None)


def build_redirect_url(token):
    return f"{BASE_URL}/email-verified/#{token}"


def fill_company_details(page):
    """Fill out UAE company details"""
    page.wait_for_selector("input[name='name']", timeout=20000)
    company_name = fake.company()
    page.fill("input[name='name']", company_name)

    page.fill("input[name='contactNumber']", "98765321")

    # Tick checkbox via JS
    page.evaluate("document.querySelector('input.PrivateSwitchBase-input[type=\"checkbox\"]').click()")

    # Select company size
    page.click("(//div[@id='company-size'])[1]")
    page.click("//p[normalize-space()='51 to 250 employees']")

    page.click("button#register-business-submit-btn")
    page.wait_for_timeout(5000)


def fill_survey(page):
    """Fill survey form"""
    team_dropdown = "//label[contains(text(), 'Select a team')]/following-sibling::div//div[@role='combobox']"
    page.click(team_dropdown)
    page.click("//li[@role='option' and @data-value='Engineering / IT']")

    role_dropdown = "//label[contains(text(), 'Select a role')]/following-sibling::div//div[@role='combobox']"
    page.click(role_dropdown)
    page.click("//li[text()='Manager']")

    page.click("(//button[normalize-space()='Save'])[1]")
    page.wait_for_selector("text=Get started", timeout=20000)


def admin_pages_check(page, expected_user_name):
    """Verify admin pages after login"""
    page.wait_for_selector("text=Get started", timeout=30000)
    assert page.is_visible("text=Home")
    assert page.is_visible("text=Card expenses")
    assert page.is_visible("text=Cards")
    assert page.is_visible("text=Requests")
    assert page.is_visible("text=Transactions")
    assert page.is_visible("text=Statements")
    assert page.is_visible("text=Accounting export")
    assert page.is_visible("text=Members & Teams")

    page.click("//span[normalize-space()='More']")
    assert page.is_visible("text=Invoices")
    assert page.is_visible("text=Reimbursements")
    assert page.is_visible("text=Budgets")
    assert page.is_visible("text=Approval policies")
    assert page.is_visible("text=Submission policies")
    assert page.is_visible("text=Receipts inbox")

    page.click("//span[normalize-space()='Settings']")
    assert page.is_visible("text=Billing")
    assert page.is_visible("text=Subscription plans")

    # Open user menu
    page.click("xpath=//span[@id='user-full-name']")
    assert page.is_visible("text=My account")
    assert page.is_visible("text=Email notifications")
    assert page.is_visible("text=Logout")

    user_name = page.inner_text("#user-full-name")
    assert expected_user_name in user_name
