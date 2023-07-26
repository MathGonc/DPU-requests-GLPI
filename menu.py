import time
import os
import random
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


def login():
    config.driver.get(config.page.get("login"))

    if len(config.userLoginName) == 0:
        WebDriverWait(config.driver, 1000).until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/nav/div/div[1]/a/img")
            )
        )  # logo dpu

        nameUser = config.driver.find_element(
            By.XPATH, '// *[ @ id = "navbar"] / ul / li[4] / a / span[1]'
        ).text
        cookies.saveCookie(nameUser.split()[0])
    """
    else:
        config.driver.find_element(By.XPATH, '//*[@id="user_login"]').send_keys(config.userLoginName)
        config.driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(config.userLoginPass)
        config.driver.find_element(By.XPATH, '//*[@id="btnEntrar"]').click()
        time.sleep(config.sleeptime)
    """


def menu_options():
    inputValue = input(
        "\nSelect an option\n"
        + "1 - Abrir & Fechar\n"
        + "2 - Abrir\n"
        + "3 - Fechar (automatico)\n"
        + "4 - Fechar (manual)\n"
        + "5 - Sair\n"
    )
    if inputValue == "1":
        menu_select_user()
        menu_OpenTypeRequest()

        openBrowser()
        user.user_login()
        user.user_logout()

        admin.admin_login()
        admin.admin_findRequestLoop()
        admin.verifyRequestExist()
        admin.closeRequest()

    elif inputValue == "2":
        menu_select_user()
        menu_OpenTypeRequest()

        openBrowser()
        user.user_login()

    elif inputValue == "3":
        config.request_manual = 0
        openBrowser()
        admin.admin_login()
        admin.closeRequest()

    elif inputValue == "4":
        config.request_manual = 1
        config.request_number = input("\nInsert request number:\n")
        openBrowser()
        admin.admin_login()
        admin.closeRequest()

    else:
        print("no option selected, exiting...")
        time.sleep(config.sleeptime)


def menu_select_user():
    # input user
    count = 1
    requestList = "\nSelect user\n" + "0 - (new user)\n"
    list = []
    for root, dirs, file in os.walk(cookies.pathCookie):
        for i in file:
            if cookies.extension in i:
                requestList = (
                    requestList
                    + str(count)
                    + " - "
                    + i.replace(cookies.extension, "")
                    + "\n"
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
    # input request
    count = 0
    requestList = "\nOpen request:\n" + "0 - (Modelo padrão)\n"
    for path in os.listdir(config.request_path):
        # check if current path is a file
        if os.path.isfile(os.path.join(config.request_path, path)):
            count += 1
            file = open(
                config.request_path + "/" + str(count) + ".txt",
                mode="r",
                encoding="utf-8",
            )
            request = file.readlines()
            requestList = requestList + str(count) + " - " + request[0]
    inputValue = input(requestList)

    match int(inputValue):
        case 0:
            config.request_manual = 1
            match (random.randint(0, 3)):
                case 0:
                    config.request_link = "https://suporte.dpu.def.br/citsmart/pages/smartPortal/smartPortal.load#/atividade/4/146/151"
                case 1:
                    config.request_link = "https://suporte.dpu.def.br/citsmart/pages/smartPortal/smartPortal.load#/atividade/4/146/152"
                case 2:
                    config.request_link = "https://suporte.dpu.def.br/citsmart/pages/smartPortal/smartPortal.load#/atividade/4/153/161"

        case _:
            # verify file request exists
            file_exists = os.path.exists(
                config.request_path + "/" + inputValue + ".txt"
            )
            if file_exists == 0:
                print("request number dont exist, exiting...")
                time.sleep(config.sleeptime)
                exit()

            file = open(
                config.request_path + "/" + inputValue + ".txt",
                mode="r",
                encoding="utf-8",
            )
            request = file.readlines()

            print("\nTipo de chamado: " + request[0])

            config.request_patrimonio = request[1]
            config.request_link = request[2]
            config.request_problem = request[3]
            config.request_class_cause = request[4]
            config.request_class_solution = request[5]
            config.request_solution = request[6]

            if len(config.request_patrimonio) <= 1:
                config.request_patrimonio = input(
                    "Este tipo de chamado exige um patrimonio: "
                )
