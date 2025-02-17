import pickle
import time

import config
from driver import driver

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

extension = ".pkl"
pathCookie = r"./users/"
cookieFile = "biscuits.pkl"
cookieAdminFile = "admin.pkl"


def saveCookie(custom):
    try:
        pickle.dump(driver.get_cookies(), open(pathCookie + custom + extension, "wb"))
        print(f"Cookie ({custom}) file successfully created.")

        if (  # Elemento que diferencia o usuario normal do admin
            len(driver.find_elements(By.XPATH, f"//div[text()='Technician']")) > 0
        ):  # detect if  user is admin
            pickle.dump(driver.get_cookies(), open(pathCookie + cookieAdminFile, "wb"))
            print("Cookie (ADMIN) file successfully created.")
    except Exception as e:
        print(e)


def loadCookie(cookieName):
    try:
        time.sleep(config.sleeptime)

        if cookieName == cookieAdminFile:
            driver.get(config.page.get("adminRequestList"))
            cookie = pickle.load(open(pathCookie + cookieAdminFile, "rb"))
            for i in cookie:
                driver.add_cookie(i)
            print("Cookies (ADMIN) added")
        else:
            driver.get(config.page.get("home"))
            cookie = pickle.load(open(pathCookie + cookieName, "rb"))
            for i in cookie:
                driver.add_cookie(i)
            print(f"Cookies ({cookieName}) added")

    except Exception as e:
        print(e)


def clearCookies():
    time.sleep(3)
    driver.delete_all_cookies()
