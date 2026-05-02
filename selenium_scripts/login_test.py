# Selenium POM Login Test Suite
# Tests against a configurable base URL
# Requires: selenium, pytest, python-dotenv

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from base_page import BasePage


class LoginPage(BasePage):
    """Page Object for Login page."""

    USERNAME_INPUT = (By.ID,   "username")
    PASSWORD_INPUT = (By.ID,   "password")
    LOGIN_BUTTON   = (By.XPATH,"//button[@type='submit']")
    ERROR_MSG      = (By.CLASS_NAME, "error-message")
    SUCCESS_MSG    = (By.CLASS_NAME, "welcome-message")
    LOGOUT_LINK    = (By.LINK_TEXT,  "Logout")

    def __init__(self, driver, base_url: str):
        super().__init__(driver)
        self.base_url = base_url

    def open(self):
        self.driver.get(f"{self.base_url}/login")
        return self

    def enter_username(self, username: str):
        self.type_text(self.USERNAME_INPUT, username)
        return self

    def enter_password(self, password: str):
        self.type_text(self.PASSWORD_INPUT, password)
        return self

    def click_login(self):
        self.click(self.LOGIN_BUTTON)
        return self

    def login(self, username: str, password: str):
        return (self.enter_username(username)
                    .enter_password(password)
                    .click_login())

    def get_error_message(self) -> str:
        return self.get_text(self.ERROR_MSG)

    def is_logged_in(self) -> bool:
        return self.is_displayed(self.SUCCESS_MSG)

    def logout(self):
        self.click(self.LOGOUT_LINK)


# ── Tests ─────────────────────────────────────────────────────────────────────
BASE_URL = "https://the-internet.herokuapp.com"


@pytest.fixture(scope="function")
def login_page(driver):
    page = LoginPage(driver, BASE_URL)
    page.open()
    return page


class TestLogin:

    def test_valid_login(self, login_page):
        login_page.login("tomsmith", "SuperSecretPassword!")
        assert login_page.is_logged_in(), "Expected to be logged in"

    def test_invalid_username(self, login_page):
        login_page.login("wronguser", "SuperSecretPassword!")
        error = login_page.get_error_message()
        assert "Your username is invalid" in error

    def test_invalid_password(self, login_page):
        login_page.login("tomsmith", "wrongpassword")
        error = login_page.get_error_message()
        assert "Your password is invalid" in error

    def test_empty_username(self, login_page):
        login_page.login("", "SuperSecretPassword!")
        assert not login_page.is_logged_in()

    def test_empty_both(self, login_page):
        login_page.login("", "")
        assert not login_page.is_logged_in()

    def test_logout_after_login(self, login_page):
        login_page.login("tomsmith", "SuperSecretPassword!")
        assert login_page.is_logged_in()
        login_page.logout()
        assert not login_page.is_logged_in()

    def test_page_title(self, login_page):
        assert "The Internet" in login_page.driver.title
