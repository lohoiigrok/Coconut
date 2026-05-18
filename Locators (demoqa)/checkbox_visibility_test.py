from playwright.sync_api import Page, expect

def test_demoqa_checkbox_visibility(page: Page):
    page.goto("https://demoqa.com/checkbox",
              wait_until="domcontentloaded",
              timeout=50000
    )

    home_item = page.locator("span.rct-title:text-is('Home')")
    desktop_item = page.locator("span.rct-title:text-is('Desktop')")

    expect(home_item).to_be_visible()
    expect(desktop_item).to_be_hidden()

    page.locator("button[title='Toggle']").click()

    expect(desktop_item).to_be_visible()
