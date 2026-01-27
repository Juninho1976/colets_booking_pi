from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os
import time

time.sleep(2)
print("🕕 Bot started at", time.strftime("%Y-%m-%d %H:%M:%S"))

load_dotenv()

# -------- CONFIG --------
CLASS_NAME = os.getenv("COLETS_CLASS_NAME")
CLASS_INDEX = 0
PAUSE = 3
MAX_ACTION_ATTEMPTS = 5
# ------------------------


EMAIL = os.getenv("COLETS_EMAIL")
PASSWORD = os.getenv("COLETS_PASSWORD")

if not CLASS_NAME:
    raise RuntimeError("Missing COLETS_CLASS_NAME in .env")

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
    print(f"✅ Logged in as {EMAIL}")
    time.sleep(PAUSE)

    # --- Open menu ---
    page.locator("#mobToggleInner span").click()
    time.sleep(PAUSE)

    # --- Navigate to timetable ---
    page.get_by_role("link", name="Classes  ").click()
    time.sleep(PAUSE)

    page.get_by_role("link", name="Fitness Classes", exact=True).click()
    time.sleep(PAUSE)

    page.get_by_role("link", name="Next→").click()
    print("➡️ Moved to next week")
    time.sleep(PAUSE)

    # --- Find class ---
    class_tiles = page.locator(
        "div[id*='ClassRepeater']:visible",
        has_text=CLASS_NAME
    )

    if class_tiles.count() <= CLASS_INDEX:
        raise RuntimeError(f"Class '{CLASS_NAME}' not found")

    class_tiles.nth(CLASS_INDEX).click()
    print(f"🟦 Opened class: {CLASS_NAME}")
    page.screenshot(path="03_class_opened.png")
    time.sleep(PAUSE)

    # --- Action loop ---
    # --- Determine primary action ---
    actions = page.locator("a.bookClassButton:visible")
    actions.wait_for(timeout=10000)

    primary_text = actions.first.inner_text().strip().lower()
    print(f"🔍 Primary action detected: {primary_text}")
    page.screenshot(path="04_primary_action.png")
    time.sleep(PAUSE)

    # --- Direct booking flow ---
    if primary_text == "book":
        print("🟢 Direct booking flow detected")

        for step in range(1, 3):
            print(f"🟢 Booking step {step}: clicking 'Book'")

            book_link = page.get_by_role("link", name="Book", exact=True)
            book_link.wait_for(timeout=15000)
            book_link.click()

            page.wait_for_load_state("networkidle")
            time.sleep(PAUSE)
            page.screenshot(path=f"05_booking_step_{step}.png")

        print(f"🎉 BOOKED: {CLASS_NAME}")
        page.screenshot(path="06_booking_complete.png")

    # --- Waiting list flow ---
    elif "waiting" in primary_text:
        print("🟡 Waiting list flow detected")

        last_action_text = None
        unchanged_count = 0

        for attempt in range(1, MAX_ACTION_ATTEMPTS + 1):
            actions = page.locator("a.bookClassButton:visible")

            if actions.count() == 0:
                print("🟡 No action buttons remain — waiting list complete")
                break

            current_text = actions.first.inner_text().strip()
            print(f"🟡 Attempt {attempt}: clicking '{current_text}'")

            actions.first.click()
            page.wait_for_load_state("networkidle")
            time.sleep(PAUSE)
            page.screenshot(path=f"05_waitlist_attempt_{attempt}.png")

            # Detect no further progress
            if current_text == last_action_text:
                unchanged_count += 1
            else:
                unchanged_count = 0

            if unchanged_count >= 2:
                print("🟡 Action no longer changing — stopping waitlist flow")
                break

            last_action_text = current_text

        print(f"🟡 WAITING LIST COMPLETED: {CLASS_NAME}")
        page.screenshot(path="06_waitlist_complete.png")

    else:
        page.screenshot(path="XX_unknown_action.png")
        raise RuntimeError(f"Unknown primary action: {primary_text}")

    browser.close()
