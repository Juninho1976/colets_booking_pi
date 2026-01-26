from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os
import time

# -------- CONFIG --------
CLASS_NAME = "PILATES IMPROVER 13+"
CLASS_INDEX = 0  # 0 = first, 1 = second
PAUSE = 5
# ------------------------

load_dotenv()

EMAIL = os.getenv("COLETS_EMAIL")
PASSWORD = os.getenv("COLETS_PASSWORD")

if not EMAIL or not PASSWORD:
    raise RuntimeError("Missing COLETS_EMAIL or COLETS_PASSWORD")

with sync_playwright() as p:
    browser = p.chromium.launch(
    headless=True,
    args=[
        "--disable-gpu",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--single-process",
    ],
    )
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
    # --- Find visible class tiles with this name ---
    class_tiles = page.locator(
        "div[id*='ClassRepeater']:visible",
        has_text=CLASS_NAME
    )

    # Safety check
    if class_tiles.count() <= CLASS_INDEX:
        raise RuntimeError(
            f"Found {class_tiles.count()} visible '{CLASS_NAME}' classes, "
            f"but CLASS_INDEX={CLASS_INDEX} is out of range"
        )

    # --- Click the chosen instance ---
    class_tiles.nth(CLASS_INDEX).click()

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