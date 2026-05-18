from playwright.sync_api import Page, expect

def test_demoqa_radio_buttons_enabled_state(page: Page):
    page.goto(
        "https://demoqa.com/radio-button",
        wait_until="domcontentloaded",
        timeout=30000
    )

    yes_radio = page.get_by_role("radio", name="Yes")
    impressive_radio = page.get_by_role("radio", name="Impressive")
    no_radio = page.get_by_role("radio", name="No")

    expect(yes_radio).to_be_enabled()
    expect(impressive_radio).to_be_enabled()
    expect(no_radio).to_be_disabled()