from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import pyautogui
import config

_driver = None  # variável interna do módulo


def get_driver():
    global _driver
    if _driver is None:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("--force-device-scale-factor=0.5")
        # chrome_options.binary_location = r"./chrome-win64/chrome.exe"

        # ChromeDriver FIXO (sem update automático)
        service = Service(r"./chromedriver-win64/chromedriver.exe")

        # 🔴 ISSO ESTAVA FALTANDO
        _driver = webdriver.Chrome(service=service, options=chrome_options)

        pyautogui.hotkey("win", "down")
        _driver.get(config.page.get("home"))

    return _driver
