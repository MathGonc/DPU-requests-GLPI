import pickle
import time

import config
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
        if (
            len(
                config.driver.find_elements(
                    By.XPATH, '// *[ @ id = "header-toolbar-access-system"] / a'
                )
            )
            > 0
        ):  # detect if  user is admin
            pickle.dump(
                config.driver.get_cookies(), open(pathCookie + cookieAdminFile, "wb")
            )
            print("Cookie admin file successfully created.")
        else:
            pickle.dump(
                config.driver.get_cookies(), open(pathCookie + custom + extension, "wb")
            )
            print("Cookie user file successfully created.")
    except Exception as e:
        print(e)


def loadCookie(cookieName):
    try:
        time.sleep(config.sleeptime)
        # config.driver.get(config.page.get("home"))  # Evitar o erro invalid cookie domain

        if cookieName == cookieAdminFile:
            cookie = pickle.load(open(pathCookie + cookieAdminFile, "rb"))
            for i in cookie:
                config.driver.add_cookie(i)
            config.driver.get(config.page.get("admin"))
            print("Cookies admin added")
        else:
            cookie = pickle.load(open(pathCookie + cookieName, "rb"))
            for i in cookie:
                config.driver.add_cookie(i)
            config.driver.get(config.page.get("oa gen"))
            print("Cookies user added")

    except Exception as e:
        print(e)
