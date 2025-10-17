# Pytest Structure Notes

## Folder Layout

```
tests/
│
├── test_login.py
├── test_registration.py
└── test_profile_update.py
```

## Example Test

```python
import pytest

def test_login_success(setup_driver):
    driver = setup_driver
    driver.get("https://demoqa.com/login")
    driver.find_element("id", "userName").send_keys("saqib")
    driver.find_element("id", "password").send_keys("demo123")
    driver.find_element("id", "login").click()
    assert "profile" in driver.current_url
```

## Fixtures

Fixtures are reusable test setup and teardown methods.

```python
@pytest.fixture
def setup_driver():
    from selenium import webdriver
    driver = webdriver.Chrome()
    yield driver
    driver.quit()
```

## Markers

```python
@pytest.mark.smoke
def test_smoke_case():
    assert True
```

## Running Tests

```bash
pytest -v --html=report.html
pytest -m smoke
pytest --maxfail=1
```

**Notes:**

* Each test should be independent.
* Group tests logically (smoke, regression, sanity).
* Use meaningful assertions.

---
