import time
import os
from configparser import ConfigParser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import config
import user
import admin
import cookies


def openBrowser():
    config.driver = webdriver.Chrome(executable_path="chromedriver")
    config.driver.maximize_window()


def openMenu():
    inputValue = input(
        "\nSelect an option\n"
        + "1 - Abrir & Fechar\n"
        + "2 - Abrir\n"
        + "3 - Fechar (automatico)\n"
        + "4 - Fechar (manual)\n"
        + "5 - Avaliar\n"
        + "6 - Fechar\n"
    )
    match (int(inputValue)):
        case 1:
            menu_select_user()
            menu_OpenTypeRequest()

            openBrowser()
            user.OpenRequest()

            admin.adminLogin()
            admin.adminFindRequestLoop()
            admin.verifyRequestExist()
            admin.requestClose()

        case 2:
            menu_select_user()
            menu_OpenTypeRequest()

            openBrowser()
            user.OpenRequest()

        case 3:
            config.request_manual = 0
            openBrowser()
            admin.adminLogin()
            admin.SelectRequestToClose()
            admin.requestClose()

        case 4:
            config.request_manual = 1
            openBrowser()
            admin.adminLogin()
            admin.SelectRequestToClose()
            admin.requestClose()

        case 5:
            config.request_manual = 1
            menu_select_user()
            openBrowser()
            user.rateRequest()

        case _:
            print("no option selected, exiting...")
            time.sleep(config.sleeptime)


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

    inputValue = input(requestList)

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


def menu_OpenTypeRequest():
    # Carregar o arquivo de configuração
    configRequest = ConfigParser()
    with open("requests.ini", "r", encoding="utf-8") as file:
        configRequest.read_file(file)

    # Montar a lista de opções
    requestList = "\nOpen request:\n0 - (Modelo padrão)\n"
    count = 1
    sections = list(configRequest.keys())
    for section in sections:
        requestList += f"{count} - {section}\n"
        count += 1

    inputValue = input(requestList)
    inputValue = int(inputValue)
    if 1 <= inputValue <= count:
        section = configRequest.sections()[inputValue - 1]
        print("\nTipo de chamado:", section)

        config.request_patrimonio = configRequest.get(section, "request_patrimonio")
        config.request_link = configRequest.get(section, "request_link")
        config.request_problem = configRequest.get(section, "request_problem")
        config.request_class_cause = configRequest.get(section, "request_class_cause")
        config.request_class_solution = configRequest.get(
            section, "request_class_solution"
        )
        config.request_solution = configRequest.get(section, "request_solution")
        config.request_knowledge = configRequest.get(section, "request_knowledge")

        if len(config.request_patrimonio) <= 1:
            config.request_patrimonio = input(
                "Este tipo de chamado exige um patrimonio: "
            )
    else:
        print("Opção inválida")
