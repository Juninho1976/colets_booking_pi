from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os
import time

# -------- CONFIG --------
CLASS_NAME = "EARLY RISE YIN & YANG YOGA 13+"
PAUSE = 5
# ------------------------

load_dotenv()

EMAIL = os.getenv("COLETS_EMAIL")
PASSWORD = os.getenv("COLETS_PASSWORD")

if not EMAIL or not PASSWORD:
    raise RuntimeError("Missing COLETS_EMAIL or COLETS_PASSWORD")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    # --- Login ---
    page.goto("https://bookings.coletshealthclub.co.uk/login.aspx")
    time.sleep(PAUSE)

    page.get_by_role("textbox", name="Email").fill(EMAIL)
    page.get_by_role("textbox", name="Password").fill(PASSWORD)
    page.get_by_role("link", name="Log In").click()
    print("✅ Logged in")

    time.sleep(PAUSE)

    # --- Open hamburger menu (IMPORTANT: span click) ---
    page.locator("#mobToggleInner span").click()
    time.sleep(PAUSE)

    # --- Navigate to Fitness Classes ---
    page.get_by_role("link", name="Classes  ").click()
    time.sleep(PAUSE)

    page.get_by_role("link", name="Fitness Classes", exact=True).click()
    time.sleep(PAUSE)

    # --- Move to next week ---
    page.get_by_role("link", name="Next→").click()
    print("➡️ Moved to next week")
    time.sleep(PAUSE)

    # --- Click class tile (EXACT ID path) ---
    page.locator(
        "div[id*='ClassRepeater']",
        has_text=CLASS_NAME
    ).first.click()

    print(f"🟦 Opened class: {CLASS_NAME}")
    time.sleep(PAUSE)

    # --- Book (first click) ---
    page.get_by_role("link", name="Book", exact=True).click()
    time.sleep(PAUSE)

    # --- Confirm booking (second click) ---
    page.get_by_role("link", name="Book", exact=True).click()

    print(f"🎉 BOOKED: {CLASS_NAME}")

    time.sleep(PAUSE)
    page.screenshot(path="booking_success.png")
    browser.close()