# Common Issues and Debugging Tips

| Issue                   | Cause                | Fix                         |
| ----------------------- | -------------------- | --------------------------- |
| Element not found       | Page not loaded yet  | Add `WebDriverWait`         |
| Stale element reference | DOM changed          | Re-locate the element       |
| Test flakiness          | Timing issues        | Use explicit waits          |
| Browser not opening     | Driver mismatch      | Install `webdriver-manager` |
| CI failures             | Headless environment | Add `--headless` in options |

## Example Wait

```python
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 10)
wait.until(EC.visibility_of_element_located((By.ID, "submit")))
```

## Logs and Reports

* Use `pytest-html` for HTML reports.
* Capture screenshots on failure.
* Save browser console logs for debugging.

## Utilities to Reuse

* `wait_for_element(locator)`
* `capture_screenshot(name)`
* `get_driver(browser_name)`

---
