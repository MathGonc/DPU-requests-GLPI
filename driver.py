from selenium import webdriver


import pyautogui
import config

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f'--app={config.page["home"]}')

chrome_options.add_argument("--start-minimized")
chrome_options.add_experimental_option("detach", True)  # Dont close
driver = webdriver.Chrome(executable_path="chromedriver", chrome_options=chrome_options)
# driver.minimize_window()
pyautogui.hotkey("win", "down")
