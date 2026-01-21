from playwright.sync_api import sync_playwright
import time

EMAIL = "YOUR_EMAIL_HERE"
PASSWORD = "YOUR_PASSWORD_HERE"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # visible for now
    page = browser.new_page()

    # Go directly to login page
    page.goto("https://bookings.coletshealthclub.co.uk/login.aspx")

    # Fill login form
    page.fill('input[type="email"], input[name*="Email"]', EMAIL)
    page.fill('input[type="password"], input[name*="Password"]', PASSWORD)

    # Optional: stay logged in
    stay_logged = page.query_selector('input[type="checkbox"]')
    if stay_logged:
        stay_logged.check()

    # Click login
    page.click('text=LOG IN')

    # Wait for navigation
    page.wait_for_load_state("networkidle")

    print("✅ Logged in successfully")

    # Pause so you can visually confirm success
    time.sleep(10)

    browser.close()