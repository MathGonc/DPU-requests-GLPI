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
        if (  # Elemento que diferencia o usuario normal do admin
            len(driver.find_elements(By.XPATH, f"//div[text()='Technician']")) > 0
        ):  # detect if  user is admin
            pickle.dump(driver.get_cookies(), open(pathCookie + cookieAdminFile, "wb"))
            print("Cookie admin file successfully created.")
        else:
            pickle.dump(
                driver.get_cookies(), open(pathCookie + custom + extension, "wb")
            )
            print("Cookie user file successfully created.")
    except Exception as e:
        print(e)


def loadCookie(cookieName):
    try:
        time.sleep(config.sleeptime)
        # driver.get(config.page.get("home"))  # Evitar o erro invalid cookie domain

        if cookieName == cookieAdminFile:
            cookie = pickle.load(open(pathCookie + cookieAdminFile, "rb"))
            for i in cookie:
                driver.add_cookie(i)
            print("Cookies admin added")
        else:
            cookie = pickle.load(open(pathCookie + cookieName, "rb"))
            for i in cookie:
                driver.add_cookie(i)
            print("Cookies user added")

    except Exception as e:
        print(e)


def clearCookies():
    driver.delete_all_cookies()
