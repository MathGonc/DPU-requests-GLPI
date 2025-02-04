from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import config
from driver import driver
import time
import user

import configparser

import tkinter as tk
from tkinter import simpledialog

root = tk.Tk()
root.withdraw()  # oculta a janela principal

ini_file = "users/pass/login.ini"
loginParser = configparser.ConfigParser()
loginParser.read(ini_file, encoding="utf-8")


def loadUserPass(name):
    print(f"Loading user password: {name}")
    if loginParser.has_section(name) == 1:
        config.userLoginName = loginParser.get(str(name), "account_login")
        config.userLoginPass = loginParser.get(str(name), "account_pass")
        print(f"{name} found")
    else:
        print(f"{name} not found")
        inputUserPass()
    return


def inputLogin():
    print("Input login")
    time.sleep(3)
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
    time.sleep(1)

    # Error 1
    element = driver.find_elements(By.XPATH, f"//*[text()='Login ou senha vazios']")
    if element:
        print("Error username and password empty")
        driver.get(config.page.get("home"))
        return inputUserPass()

    # Error 2
    element = driver.find_elements(
        By.XPATH, f"//*[text()='Nome de usuário ou senha inválidos']"
    )
    if element:
        print("Error password")
        driver.get(config.page.get("home"))
        return inputUserPass()

    # Error 3
    element = driver.find_elements(By.XPATH, f"//*[text()='Return to previous page']")
    if element:
        print("Error login page")
        driver.get(config.page.get("home"))
        return inputLogin()

    return 1


def inputUserPass():
    config.userLoginName = simpledialog.askstring("Login", "Digite seu usuário:")
    config.userLoginPass = simpledialog.askstring(
        "Senha", "Digite sua senha:", show="*"
    )

    print(f"usuário: {config.userLoginName}, senha: {config.userLoginPass}")
    inputLogin()
    return 1


def saveUserPass(name):

    if not loginParser.has_section(name):
        loginParser.add_section(name)
    loginParser.set(name, "account_login", config.userLoginName)
    loginParser.set(name, "account_pass", config.userLoginPass)
    with open(ini_file, "w", encoding="utf-8") as loginfile:
        loginParser.write(loginfile)
    print(f"Account {name} save in .ini")
    return
