from selenium import webdriver

from webdriver_auto_update.chrome_app_utils import ChromeAppUtils
from webdriver_auto_update.webdriver_manager import WebDriverManager

import pyautogui
import config

# Auto update chrome
chrome_app_utils = ChromeAppUtils()
chrome_app_version = chrome_app_utils.get_chrome_version()
print("Chrome application version: ", chrome_app_version)
driver_directory = ""
driver_manager = WebDriverManager(driver_directory)
driver_manager.main()

# Open browser
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f'--app={config.page["home"]}')

chrome_options.add_argument("--start-minimized")
chrome_options.add_experimental_option("detach", True)  # Dont close
driver = webdriver.Chrome(
    executable_path="chromedriver", chrome_options=chrome_options
)  # https://googlechromelabs.github.io/chrome-for-testing/
# driver.minimize_window()
pyautogui.hotkey("win", "down")
