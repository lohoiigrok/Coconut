from playwright.sync_api import Page, expect
from random import randint

def test_text_box(page: Page):
    page.goto('https://demoqa.com/text-box')

    # вариант №1
    username_locator = '#userName'
    page.fill(username_locator, 'testQa')
    page.fill('#userEmail', 'test@qa.com')
    page.fill('#currentAddress', 'Phuket, Thalang 99')
    page.fill('#permanentAddress', 'Moscow, Mashkova 1')

    page.click('button#submit')

    expect(page.locator('#output #name')).to_have_text('Name:testQa')
    expect(page.locator('#output #email')).to_have_text('Email:test@qa.com')
    expect(page.locator('#output #currentAddress')).to_have_text('Current Address :Phuket, Thalang 99')
    expect(page.locator('#output #permanentAddress')).to_have_text('Permanent Address :Moscow, Mashkova 1')

def test_registration(page: Page):
    page.goto('https://dev-cinescope.coconutqa.ru/register')

    # вариант №1
    username_locator = '[data-qa-id="register_full_name_input"]'
    email_locator = '[data-qa-id="register_email_input"]'
    password_locator = '[data-qa-id="register_password_input"]'
    repeat_password_locator = '[data-qa-id="register_password_repeat_input"]'

    user_email = f'test{randint(1, 9999)}-admin@email.qa'

    page.fill(username_locator, 'Жмышенко Валерий Альбертович')
    page.fill(email_locator, user_email)
    page.fill(password_locator, 'qwerty123Q')
    page.fill(repeat_password_locator, 'qwerty123Q')

    page.click('[data-qa-id="register_submit_button"]')

    page.wait_for_url('https://dev-cinescope.coconutqa.ru/login')
    expect(page.get_by_text("Подтвердите свою почту")).to_be_visible(visible=True)
