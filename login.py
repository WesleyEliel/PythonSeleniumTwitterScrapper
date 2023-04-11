from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import logging
import time

logger = logging.getLogger(__name__)


class Login():
    def __init__(self, browser, username: str, password: str) -> None:
        self.browser = browser
        self.username = username
        self.password = password
        self._baseUrl = 'https://www.twitter.com/login'

    def log_message(self, message):
        logger.info(f'\n\n { message } \n\n')

    def login(self):
        self.log_message("Waiting for Browser")
        wait = WebDriverWait(self.browser, 40)
        self.browser.get(self._baseUrl)
        self.log_message("Loking for Username Input")
        username_input = wait.until(
            EC.visibility_of_element_located((By.NAME, "text")))
        self.log_message("Sending Keys to Username Input")
        username_input.send_keys(self.username)
        self.log_message("Found Username Input")
        time.sleep(3)
        username_input.send_keys(Keys.ENTER)
        self.log_message("Waiting for Browser")
        time.sleep(10)
        self.log_message("Loking for Password Input")
        password_input = wait.until(
            EC.visibility_of_element_located((By.NAME, "password")))
        self.log_message("Sending Keys to Password Input")
        password_input.send_keys(self.password)
        password_input.send_keys(Keys.ENTER)
        time.sleep(7)
        return self.browser
