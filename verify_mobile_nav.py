from playwright.sync_api import sync_playwright, expect

def test_mobile_nav():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Use a mobile viewport
        context = browser.new_context(viewport={'width': 375, 'height': 667})
        page = context.new_page()

        # Navigate to the local server
        page.goto("http://localhost:5173")
        page.wait_for_timeout(2000) # wait for render

        # Take initial screenshot
        page.screenshot(path="/app/mobile_nav_initial.png")

        # Verify theme button exists with the expected aria-label prefix
        theme_button = page.get_by_role("button", name="Theme: system (light)")
        if theme_button.count() == 0:
             theme_button = page.get_by_role("button", name="Theme: system (dark)")
        expect(theme_button.first).to_be_visible()

        # Verify menu button exists with 'Open menu' label
        menu_button = page.get_by_role("button", name="Open menu")
        expect(menu_button.first).to_be_visible()

        # Click menu button
        menu_button.first.click()
        page.wait_for_timeout(1000)

        # Take screenshot of open menu
        page.screenshot(path="/app/mobile_nav_open.png")

        browser.close()

if __name__ == "__main__":
    test_mobile_nav()
