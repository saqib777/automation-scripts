# Browser Automation Examples

## 1. Opening and Validating a Website

This script validates the title of the website to confirm it loaded correctly.

```python
from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://demoqa.com")
assert "ToolsQA" in driver.title
driver.quit()
```

## 2. Automating Form Submission

```python
driver.get("https://demoqa.com/automation-practice-form")
driver.find_element("id", "firstName").send_keys("Mohammed")
driver.find_element("id", "lastName").send_keys("Saqib")
driver.find_element("id", "userEmail").send_keys("saqib@example.com")
driver.find_element("id", "submit").click()
```

## 3. Handling Alerts

```python
alert_button = driver.find_element("id", "alertButton")
alert_button.click()
alert = driver.switch_to.alert
print(alert.text)
alert.accept()
```

## 4. Uploading Files

```python
file_input = driver.find_element("id", "uploadFile")
file_input.send_keys("C:\\path\\to\\resume.pdf")
```

## 5. Capturing Screenshots

```python
driver.save_screenshot("form_result.png")
```

---

**Notes:**

* Always wrap critical steps in `try-except` blocks.
* Use **implicit** or **explicit waits** for dynamic elements.
* Store selectors in a constants file for reusability.

---
