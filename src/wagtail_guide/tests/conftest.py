import os

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from wagtail_guide.conf import conf


class ShortcutMixin:
    def click_link(self, link_text):
        self.find_element(By.LINK_TEXT, link_text).click()

    def click_button(self, button_text):
        self.find_element(By.XPATH, f"//button[text()='{button_text}']").click()

    def clear_input(self, field_name):
        self.find_element(By.NAME, field_name).clear()

    def input_text(self, field_name, text):
        self.find_element(By.NAME, field_name).send_keys(text)

    def scroll_to_bottom(self):
        self.execute_script("window.scrollTo(0, document.body.scrollHeight);")


class RemoteDriver(ShortcutMixin, webdriver.Remote):
    pass


class ChromeDriver(ShortcutMixin, webdriver.Chrome):
    pass


@pytest.fixture
def driver():
    """Provide a selenium webdriver instance, and tear down after use."""
    options = webdriver.ChromeOptions()
    options.add_argument("--force-device-scale-factor=2")
    options.add_argument("--no-sandbox")  # Bypass OS security model

    if os.environ.get("HEADLESS"):
        # docker run -d -p 4444:4444 --shm-size=2g selenium/standalone-chrome:3.141.59  # Intel Silicon
        # docker run -d -p 4444:4444 --shm-size="2g" seleniarm/standalone-chromium  # Apple Silicon
        url = os.environ.get("SELENIUM_REMOTE_URL", "http://127.0.0.1:4444")
        driver = RemoteDriver(
            url, desired_capabilities=DesiredCapabilities.CHROME, options=options
        )
    else:
        driver = ChromeDriver(
            conf.SELENIUM_CHROMEDRIVER_EXECUTABLE_PATH, options=options
        )

    driver.set_window_size(1024, 768)
    yield driver
    # Tear down
    driver.quit()
