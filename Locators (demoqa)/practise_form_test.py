from datetime import datetime
from pathlib import Path
from playwright.sync_api import Page, expect

def test_demoqa_practice_form(page: Page):
    page.goto(
        "https://demoqa.com/automation-practice-form",
        wait_until="domcontentloaded",
        timeout=30000
    )

    # Проверка даты по умолчанию == сегодня
    dob_value = page.get_attribute("#dateOfBirthInput", "value")
    today_value = datetime.now().strftime("%d %b %Y")
    assert dob_value == today_value, f"Ожидали {today_value}, получили {dob_value}"

    # Проверка текста футера
    footer_text = page.locator("footer").text_content()
    assert footer_text is not None
    assert footer_text.strip() == "© 2013-2020 TOOLSQA.COM | ALL RIGHTS RESERVED."

    # fill() — быстрое заполнение целиком
    page.fill("#firstName", "Ivan")
    page.fill("#lastName", "Petrov")

    # type() — имитация ввода по символам
    page.type("#userEmail", "ivan.petrov@test.com")
    page.type("#userNumber", "9991234567")

    # Radio button через label
    page.locator('[for="gender-radio-1"]').click()

    # Date of Birth
    page.click("#dateOfBirthInput")
    page.locator(".react-datepicker__year-select").select_option("1995")
    page.locator(".react-datepicker__month-select").select_option(label="December")
    page.locator(".react-datepicker__day--010:not(.react-datepicker__day--outside-month)").click()

    expect(page.locator("#dateOfBirthInput")).to_have_value("10 Dec 1995")

    # Subjects
    page.locator("#subjectsInput").fill("Maths")
    page.locator("#subjectsInput").press("Enter")
    page.locator("#subjectsInput").fill("English")
    page.locator("#subjectsInput").press("Enter")

    # Checkboxes через label
    page.locator('[for="hobbies-checkbox-1"]').click()  # Sports
    page.locator('[for="hobbies-checkbox-2"]').click()  # Reading

    # Upload picture
    file_path = Path("test_data.txt")
    file_path.write_text("demo file", encoding="utf-8")
    page.set_input_files("#uploadPicture", str(file_path))

    # Address
    page.fill("#currentAddress", "Amsterdam, QA street 10")

    # State
    page.locator("#state").click()
    page.locator("#react-select-3-input").fill("NCR")
    page.locator("#react-select-3-input").press("Enter")

    # City
    page.locator("#city").click()
    page.locator("#react-select-4-input").fill("Delhi")
    page.locator("#react-select-4-input").press("Enter")

    # Submit
    page.locator("#submit").click()

    # Проверка результата
    expect(page.locator("#example-modal-sizes-title-lg")).to_have_text("Thanks for submitting the form")
    expect(page.locator(".table-responsive")).to_contain_text("Ivan Petrov")
    expect(page.locator(".table-responsive")).to_contain_text("ivan.petrov@test.com")
    expect(page.locator(".table-responsive")).to_contain_text("Male")
    expect(page.locator(".table-responsive")).to_contain_text("9991234567")
    expect(page.locator(".table-responsive")).to_contain_text("10 December,1995")
    expect(page.locator(".table-responsive")).to_contain_text("Maths, English")
    expect(page.locator(".table-responsive")).to_contain_text("Sports, Reading")
    expect(page.locator(".table-responsive")).to_contain_text("test_data.txt")
    expect(page.locator(".table-responsive")).to_contain_text("Amsterdam, QA street 10")
    expect(page.locator(".table-responsive")).to_contain_text("NCR Delhi")
