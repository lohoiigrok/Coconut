from playwright.sync_api import Page, expect

def test_add_new_record_to_webtable(page: Page):
    page.goto(
        "https://demoqa.com/webtables",
        wait_until="domcontentloaded",
        timeout=30000
    )

    page.locator("button:has-text('Add')").click()

    expect(
        page.locator("div.modal-content").get_by_text("Registration Form")
    ).to_be_visible()

    page.locator('input[placeholder="First Name"]').fill("Ivan")
    page.locator('input[placeholder="Last Name"]').fill("Petrov")
    page.locator('input[placeholder="name@example.com"]').fill("ivan.petrov@test.com")
    page.locator('input[placeholder="Age"]').fill("30")
    page.locator('input[placeholder="Salary"]').fill("10000")
    page.locator('input[placeholder="Department"]').fill("QA")

    page.locator("button[type='submit']").click()

    expect(page.locator("div.modal-content")).to_be_hidden()

    page.locator("#searchBox").fill("ivan.petrov@test.com")

    expect(page.get_by_text("ivan.petrov@test.com", exact=True)).to_be_visible()
    expect(page.get_by_text("Ivan", exact=True)).to_be_visible()
    expect(page.get_by_text("10000", exact=True)).to_be_visible()
    expect(page.get_by_text("Petrov", exact=True)).to_be_visible()
    expect(page.get_by_text("QA", exact=True)).to_be_visible()