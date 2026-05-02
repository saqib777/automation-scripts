# Automation Scripts

A production-grade test automation framework covering Selenium UI tests,
REST API tests, CI/CD integration, and utilities - built in Python.

---

## Structure

```
automation-scripts/
├── selenium_scripts/
│   ├── base_page.py           # Reusable BasePage class (POM)
│   ├── driver_factory.py      # Chrome/Firefox factory
│   ├── login_test.py          # Login page test suite
│   └── form_fill_test.py      # Form automation suite
├── api_scripts/
│   ├── api_base.py            # Requests wrapper with logging
│   ├── test_jsonplaceholder.py# Public API full CRUD tests
│   ├── test_reqres_api.py     # ReqRes API CRUD + auth tests
│   ├── schema_validator.py    # Pure Python JSON schema validator
│   └── test_schema_validator.py
├── ci_helpers/
│   └── generate_report.py     # pytest HTML + JSON report runner
├── utilities/
│   ├── config.py              # Env-var config loader
│   └── logger.py              # Rotating file + console logger
├── .github/workflows/
│   └── run_tests.yml          # GitHub Actions CI pipeline
├── conftest.py                # Shared fixtures + screenshot on fail
├── requirements.txt
└── README.md
```

---

## Setup

```bash
pip install -r requirements.txt
```

Create a `.env` file (optional):

```
BASE_URL=https://the-internet.herokuapp.com
API_BASE_URL=https://reqres.in/api
BROWSER=chrome
HEADLESS=true
EXPLICIT_WAIT=10
```

---

## Running Tests

```bash
# All tests
pytest -v

# API tests only
pytest api_scripts/ -v

# Selenium tests only
pytest selenium_scripts/ -v

# With HTML report
pytest --html=reports/report.html --self-contained-html

# Specific test class
pytest selenium_scripts/login_test.py::TestLogin -v

# Generate full report
python ci_helpers/generate_report.py --path api_scripts/
```

---

## CI/CD

GitHub Actions runs automatically on:
- Every push to `main` or `develop`
- Every pull request to `main`
- Daily at 6:00 AM UTC

Reports are uploaded as workflow artifacts after each run.

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.11 | Primary language |
| pytest | Test runner and assertions |
| Selenium 4 | Browser automation |
| requests | API testing |
| pytest-html | HTML test reports |
| GitHub Actions | CI/CD pipeline |

---

## Author

Mohammed Saqib — github.com/saqib777 — Bengaluru, India
