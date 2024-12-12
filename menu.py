import time
import os
from configparser import ConfigParser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import config
import user
import admin
import cookies
import utils
from driver import driver, chrome_options


def startBrowserUse():
    if utils.verifyBrowserIsOpen():
        driver.maximize_window()
        driver.delete_all_cookies()
    else:
        reopenBrowser()


def reopenBrowser():
    driver = webdriver.Chrome(
        executable_path="chromedriver", chrome_options=chrome_options
    )
    driver.maximize_window()


def openMenu():
    if config.defaultOption == 0:
        inputValue = input(
            "\nSelect an option\n"
            + "1 - Abrir & Fechar\n"
            + "2 - Abrir\n"
            + "3 - Fechar (automatico)\n"
            + "4 - Fechar (manual)\n"
            + "5 - Avaliar\n"
            + "6 - Fechar\n"
        )
    else:
        inputValue = config.defaultOption

    match (int(inputValue)):
        case 1:
            menu_select_user()
            menuSelectTypeRequest()

            startBrowserUse()
            user.OpenRequest()

            admin.adminLogin()
            admin.adminFindRequestLoop()
            admin.verifyRequestExist()
            admin.SelectRequestToClose()
            admin.requestClose()

        case 2:
            menu_select_user()
            menuSelectTypeRequest()

            startBrowserUse()
            user.OpenRequest()
            driver.close()  # Não usar na função de abrir e fechar

        case 3:
            utils.setManualMode(0)
            startBrowserUse()
            admin.adminLogin()
            admin.SelectRequestToClose()
            admin.requestClose()

        case 4:
            utils.setManualMode(1)
            startBrowserUse()
            admin.adminLogin()
            admin.SelectRequestToClose()
            admin.requestClose()

        case 5:
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
        inputValue = input(requestList)
    else:
        inputValue = config.defaultUser

    if int(inputValue) > 0:
        count = 1
        list = []
        for root, dirs, file in os.walk(cookies.pathCookie):
            for i in file:
                if cookies.extension in i:
                    if int(inputValue) == count:
                        config.userLoginName = i.replace(cookies.extension, "")
                        print("user: " + i)
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
        inputValue = input(requestList)
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
                config.request_patrimonio = input(
                    "Este tipo de chamado exige um patrimonio: "
                )
            else:
                config.request_patrimonio = config.defaultPatrimonio
    elif inputValue == 0:
        return
    else:
        print("Opção inválida")


def menuReset():
    driver.quit()
    inputValue = input("\nSelect an option\n" + "1 - Repetir\n" + "2 - Fechar\n")
    if int(inputValue) == 1:
        openMenu()
    else:
        quit()
