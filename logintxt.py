from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import config
from driver import driver
import time

from configparser import ConfigParser

configparser = ConfigParser()
configparser.read("users\pass\login.ini", encoding="utf-8")


def loadUserPass(name):
    print(f"Loading user password: {name}")
    config.userLoginName = configparser.get(str(name), "account_login")
    config.userLoginPass = configparser.get(str(name), "account_pass")
    return


def inputLogin():
    element = WebDriverWait(driver, 99999).until(
        EC.element_to_be_clickable(
            (
                By.CSS_SELECTOR,
                "#login_name",
            )
        )
    )
    element.send_keys(config.userLoginName)

    element = WebDriverWait(driver, 99999).until(
        EC.element_to_be_clickable(
            (
                By.CSS_SELECTOR,
                "#login_password",
            )
        )
    )
    element.send_keys(config.userLoginPass)

    element = WebDriverWait(driver, 99999).until(
        EC.element_to_be_clickable(
            (
                By.CSS_SELECTOR,
                "body > div.page-anonymous > div > div > div.card.card-md > div > form > div > div > div.form-footer > button",
            )
        )
    )
    element.click()

    # Verify error and try again
    WebDriverWait(driver, 99999).until(  # Wait login button dissaper
        EC.invisibility_of_element_located(
            (
                By.CSS_SELECTOR,
                "body > div.page-anonymous > div > div > div.card.card-md > div > form > div > div > div.form-footer > button",
            )
        )
    )
    element = driver.find_elements(By.XPATH, f"//*[text()='Return to previous page']")
    if element:
        element[0].click()
        WebDriverWait(driver, 99999).until(  # Wait login button dissaper
            EC.invisibility_of_element_located(
                (
                    By.XPATH,
                    "//*[text()='Return to previous page']",
                )
            )
        )
        inputLogin()


def saveUserPass():
    return
