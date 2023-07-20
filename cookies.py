import pickle

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
        config.driver.get(config.page.get("login"))
        if cookieName == cookieAdminFile:
            cookie = pickle.load(
                open(pathCookie + cookieAdminFile, "rb")
            )  # loading from pickle file
        else:
            cookie = pickle.load(
                open(pathCookie + cookieName, "rb")
            )  # loading from pickle file
        for i in cookie:
            config.driver.add_cookie(i)
        print("Cookies admin added.")
    except Exception as e:
        print(e)
