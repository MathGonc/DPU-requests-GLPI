import time
import os
from configparser import ConfigParser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


import tkinter as tk
from tkinter import simpledialog

import config
import user
import admin
import cookies
import utils
import logintxt


import driver

driver = driver.get_driver()


def startBrowserUse():
    if utils.verifyBrowserIsOpen():
        driver.maximize_window()
        driver.delete_all_cookies()
    else:
        reopenBrowser()


# def reopenBrowser():
#     driver = webdriver.Chrome(
#         executable_path="chromedriver", chrome_options=chrome_options
#     )
#     driver.maximize_window()


def selectMenuOptions(option):

    match (int(option)):
        case 0:
            utils.setManualMode(0)
            startBrowserUse()
            user.login(1)
            time.sleep(99999)
        case 1:
            menu_select_user()
            menuSelectTypeRequest()

            utils.setManualMode(0)
            startBrowserUse()
            user.OpenRequest()

            user.login(1)
            admin.SelectRequestToClose()
            admin.requestClose()

        case 2:
            menu_select_user()
            menuSelectTypeRequest()

            utils.setManualMode(0)
            startBrowserUse()
            user.OpenRequest()
            driver.close()  # Não usar na função de abrir e fechar

        case 3:
            utils.setManualMode(0)
            startBrowserUse()
            user.login(1)
            admin.SelectRequestToClose()
            admin.requestClose()

        case 4:  # TO DO: close manual function
            utils.setManualMode(1)
            startBrowserUse()
            user.login(1)
            admin.SelectRequestToClose()
            admin.requestClose()

        case 5:  # TO DO: rate function
            utils.setManualMode(1)
            menu_select_user()
            startBrowserUse()
            user.rateRequest()

        case _:
            print("no option selected, exiting...")
            time.sleep(config.sleeptime)

    menuReset()


def menu_select_user():
    # input user
    count = 1
    requestList = f"\nSelect user\n 0 - (new user)\n"
    list = []
    for root, dirs, file in os.walk(cookies.pathCookie):
        for i in file:
            if cookies.extension in i:
                requestList = (
                    f"{requestList} {count} - {i.replace(cookies.extension, '')}\n"
                )
                count += 1

    if config.defaultUser == 0:
        inputValue = simpledialog.askstring("Options", requestList)
    else:
        inputValue = config.defaultUser

    if int(inputValue) > 0:
        count = 1
        list = []
        for root, dirs, file in os.walk(cookies.pathCookie):
            for i in file:
                if cookies.extension in i:
                    if int(inputValue) == count:
                        config.userName = i.replace(cookies.extension, "")
                        if config.saveLoginTxt == 1:
                            logintxt.loadUserPass(config.userName)
                        print("user: " + config.userName)
                        return 1
                count += 1
        print("user dont exists, exiting...")
        exit()


def menuSelectTypeRequest():
    # Carregar o arquivo de configuração
    configRequest = ConfigParser()
    with open("requests.ini", "r", encoding="utf-8") as file:
        configRequest.read_file(file)

    # Montar a lista de opções
    requestList = "\nOpen request:\n"
    count = 1
    sections = list(configRequest.keys())
    for section in sections:
        if section == "DEFAULT":
            requestList += f"0 - (Modelo padrão)\n"
        else:
            requestList += f"{count} - {section}\n"
            count += 1

    if config.defaultRequest == 0:
        inputValue = simpledialog.askstring("Options", requestList)
        inputValue = int(inputValue)
    else:
        inputValue = config.defaultRequest

    if 1 <= inputValue <= count:
        section = configRequest.sections()[inputValue - 1]
        print("\nTipo de chamado:", section)

        config.request_title = section
        config.request_patrimonio = configRequest.get(section, "request_patrimonio")
        config.request_link = configRequest.get(section, "request_link")
        config.request_problem = configRequest.get(section, "request_problem")
        config.request_category = configRequest.get(section, "request_category")
        config.request_class_solution = configRequest.get(
            section, "request_class_solution"
        )
        config.request_solution = configRequest.get(section, "request_solution")
        config.request_knowledge = configRequest.get(section, "request_knowledge")

        if len(config.request_patrimonio) <= 1:
            if config.defaultPatrimonio == 0:
                config.request_patrimonio = simpledialog.askstring(
                    "Este tipo de chamado exige um patrimonio: ", ""
                )
            else:
                config.request_patrimonio = config.defaultPatrimonio
    elif inputValue == 0:
        return
    else:
        print("Opção inválida")


def menuReset():
    driver.quit()
    inputValue = simpledialog.askstring(
        "", "\nSelect an option\n" + "1 - Repetir\n" + "2 - Fechar\n"
    )
    if int(inputValue) == 1:
        openMenu()
    else:
        quit()
