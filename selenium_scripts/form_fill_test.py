# Selenium Form Fill Automation
# Tests form inputs, dropdowns, checkboxes, file upload

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from base_page import BasePage


class FormPage(BasePage):
    """Page Object for a general HTML form."""

    FIRST_NAME   = (By.ID, "firstname")
    LAST_NAME    = (By.ID, "lastname")
    EMAIL        = (By.ID, "email")
    PHONE        = (By.ID, "phone")
    GENDER_MALE  = (By.XPATH, "//input[@value='male']")
    COUNTRY_DROP = (By.ID, "country")
    HOBBY_SPORTS = (By.XPATH, "//input[@value='sports']")
    HOBBY_MUSIC  = (By.XPATH, "//input[@value='music']")
    SUBMIT_BTN   = (By.ID, "submit")
    SUCCESS_MSG  = (By.ID, "success-message")
    ERROR_MSGS   = (By.CLASS_NAME, "field-error")

    def fill_personal_info(self, first, last, email, phone):
        self.type_text(self.FIRST_NAME, first)
        self.type_text(self.LAST_NAME,  last)
        self.type_text(self.EMAIL,      email)
        self.type_text(self.PHONE,      phone)
        return self

    def select_gender(self, gender="male"):
        if gender == "male":
            self.click(self.GENDER_MALE)
        return self

    def select_country(self, country: str):
        dropdown = Select(self.driver.find_element(*self.COUNTRY_DROP))
        dropdown.select_by_visible_text(country)
        return self

    def select_hobby(self, hobby: str):
        if hobby == "sports":
            self.click(self.HOBBY_SPORTS)
        elif hobby == "music":
            self.click(self.HOBBY_MUSIC)
        return self

    def submit(self):
        self.click(self.SUBMIT_BTN)
        return self

    def get_success(self) -> str:
        return self.get_text(self.SUCCESS_MSG)


BASE_URL = "https://demoqa.com/automation-practice-form"


@pytest.fixture
def form(driver):
    driver.get(BASE_URL)
    return FormPage(driver)


class TestFormFill:

    def test_complete_form_submission(self, form):
        (form.fill_personal_info("Mohammed", "Saqib", "saqib@test.com", "9876543210")
             .select_gender()
             .select_hobby("sports")
             .submit())
        assert form.is_displayed(form.SUCCESS_MSG)

    def test_required_fields_empty(self, form):
        form.submit()
        assert not form.is_displayed(form.SUCCESS_MSG)

    def test_invalid_email_format(self, form):
        form.fill_personal_info("Test", "User", "notanemail", "9876543210")
        form.submit()
        assert not form.is_displayed(form.SUCCESS_MSG)

    def test_phone_accepts_digits(self, form):
        form.type_text(form.PHONE, "1234567890")
        val = form.driver.find_element(*form.PHONE).get_attribute("value")
        assert val == "1234567890"

    def test_gender_radio_selectable(self, form):
        form.select_gender("male")
        radio = form.driver.find_element(*form.GENDER_MALE)
        assert radio.is_selected()

    def test_hobby_checkbox_selectable(self, form):
        form.select_hobby("sports")
        checkbox = form.driver.find_element(*form.HOBBY_SPORTS)
        assert checkbox.is_selected()

    def test_multiple_hobbies_selectable(self, form):
        form.select_hobby("sports")
        form.select_hobby("music")
        assert form.driver.find_element(*form.HOBBY_SPORTS).is_selected()
        assert form.driver.find_element(*form.HOBBY_MUSIC).is_selected()
