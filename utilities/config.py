# Config loader for automation-scripts
# Loads settings from environment variables with sensible defaults
# Supports .env file via python-dotenv

import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass   # dotenv optional — use system env vars directly


class Config:
    """
    Central configuration for all test suites.
    Values read from environment variables with defaults.

    Usage:
        from utilities.config import Config
        cfg = Config()
        driver.get(cfg.BASE_URL)
    """

    # ── URLs ──────────────────────────────────────────────────────────────────
    BASE_URL       = os.getenv("BASE_URL",       "https://the-internet.herokuapp.com")
    API_BASE_URL   = os.getenv("API_BASE_URL",   "https://reqres.in/api")
    DEMO_URL       = os.getenv("DEMO_URL",       "https://demoqa.com")

    # ── Browser ───────────────────────────────────────────────────────────────
    BROWSER        = os.getenv("BROWSER",        "chrome").lower()
    HEADLESS       = os.getenv("HEADLESS",       "true").lower() == "true"
    IMPLICIT_WAIT  = int(os.getenv("IMPLICIT_WAIT",  "5"))
    EXPLICIT_WAIT  = int(os.getenv("EXPLICIT_WAIT",  "10"))
    PAGE_LOAD_TIMEOUT = int(os.getenv("PAGE_LOAD_TIMEOUT", "30"))

    # ── Credentials ───────────────────────────────────────────────────────────
    TEST_USERNAME  = os.getenv("TEST_USERNAME",  "tomsmith")
    TEST_PASSWORD  = os.getenv("TEST_PASSWORD",  "SuperSecretPassword!")
    API_KEY        = os.getenv("API_KEY",        "")

    # ── Reporting ─────────────────────────────────────────────────────────────
    REPORT_DIR     = os.getenv("REPORT_DIR",     "reports")
    SCREENSHOT_DIR = os.getenv("SCREENSHOT_DIR", "screenshots")
    LOG_LEVEL      = os.getenv("LOG_LEVEL",      "INFO")

    # ── Retry ─────────────────────────────────────────────────────────────────
    MAX_RETRIES    = int(os.getenv("MAX_RETRIES", "3"))
    RETRY_DELAY    = float(os.getenv("RETRY_DELAY", "1.0"))

    @classmethod
    def summary(cls) -> str:
        return (
            f"Config Summary:\n"
            f"  BASE_URL:    {cls.BASE_URL}\n"
            f"  BROWSER:     {cls.BROWSER}\n"
            f"  HEADLESS:    {cls.HEADLESS}\n"
            f"  EXPLICIT_WAIT: {cls.EXPLICIT_WAIT}s\n"
            f"  REPORT_DIR:  {cls.REPORT_DIR}\n"
        )

    @classmethod
    def validate(cls):
        """Raise ValueError if critical config is missing."""
        required = {"BASE_URL": cls.BASE_URL, "API_BASE_URL": cls.API_BASE_URL}
        for key, val in required.items():
            if not val:
                raise ValueError(f"Missing required config: {key}")


if __name__ == "__main__":
    print(Config.summary())
    Config.validate()
    print("Config valid.")
