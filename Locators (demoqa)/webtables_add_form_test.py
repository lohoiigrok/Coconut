from playwright.sync_api import Page, expect

def test_demoqa_webtables_add_form(page: Page):
    page.goto(
        "https://demoqa.com/webtables",
        wait_until="domcontentloaded",
        timeout=30000
    )

    # <button> с текстом "Add"
    add_button = page.locator("button:has-text('Add')")
    expect(add_button).to_be_visible()
    add_button.click()

    # Проверяем, что форма открылась (заголовок "Registration Form")
    modal_title = page.locator(
        "div.modal-content div.modal-header div:has-text('Registration Form')"
    )
    expect(modal_title).to_be_visible()

    # Первый инпут по placeholder "First Name"
    first_name_input = page.locator('input[placeholder="First Name"]')
    first_name_input.fill("Ivan")

    # Остальные поля - любыми удобными CSS-селекторами
    page.locator('input[placeholder="Last Name"]').fill("Petrov")
    page.locator('input[placeholder="Salary"]').fill("10000")
    page.locator('input[placeholder="Department"]').fill("QA")

    # Кнопка Submit - по type и тексту
    submit_button = page.locator("button[type='submit']:has-text('Submit')")
    submit_button.click()

    # Можно добавить легкую проверку, что модалка закрылась
    expect(modal_title).to_be_hidden()
