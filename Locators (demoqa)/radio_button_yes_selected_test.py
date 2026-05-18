from playwright.sync_api import Page, expect

def radio_button_yes_selected_test(page: Page):
    page.goto("https://demoqa.com/radio-button",
              wait_until="domcontentloaded", timeout=30000)

    yes_radio = page.get_by_role("radio", name="Yes")

    impressive_radio = page.get_by_role("radio", name="Impressive")
    no_radio = page.get_by_role("radio", name="No")

    expect(yes_radio).to_be_enabled()
    expect(impressive_radio).to_be_enabled()
    expect(no_radio).to_be_disabled()

    page.locator('[for="yesRadio"]').click()

    expect(yes_radio).to_be_checked()
    expect(impressive_radio).not_to_be_checked()
    expect(page.locator(".text-success")).to_have_text("Yes")
