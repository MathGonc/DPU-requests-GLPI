import random
import os
from configparser import ConfigParser

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import config
import menu
import cookies
import utils

xpathSuspended = '//*[@id="radio-request-suspensa"]'
xpathReactive = '//*[@id="request-reactivate"]'
xpathSolution = "/html/body/div[3]/div/div[2]/div/div[1]/div/form/div/div/div/div/div/div[2]/div/div/div[3]/div[2]/div[6]/div/fieldset/div[4]/div[2]/div/div/citsmart-trix-editor/div/trix-editor"
xpathNameUser = '//*[@id="service-request-view"]/div/div/div/div[2]/div/div/div[3]/div[1]/div[1]/div/fieldset/div[1]/div[1]/div/div[2]'
xpathRequestPatrominio = "/html/body/div[3]/div/div[2]/div/div[1]/div/form/div/div/div/div/div/div[2]/div/div/div[3]/div[2]/div[3]/div/fieldset/div/div/div[2]/div[2]/div/div/input"
xpathRequestCaptureTicket = '//*[@id="service-request-view"]/div/div/div/div[1]/div/ul/li[4]/div[1]/div[2]/div[2]/span/a'
xpathRequestLoading = (
    '//*[@id="divCorpoJanelaAguarde_JANELA_AGUARDE_MENU"]/table/tbody/tr/td'
)

xpathPageRequestList = '//*[@id="service-request-incident-container"]/div[1]'
xpathPageRequestReview = '//*[@id="service-request-view"]/div/div/div/div[1]/div'


def adminLogin():
    cookies.loadCookie(cookies.cookieAdminFile)
    config.driver.get(config.page["admin"])
    WebDriverWait(config.driver, 9999).until(
        EC.presence_of_element_located((By.XPATH, xpathPageRequestList))
    )


def adminFindRequestLoop():
    # config.driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div/div[1]/div/form/div/div[2]/div[1]/div[2]/button[2]/i').click() #click in refresh and wait

    requestItem = "list-item-" + config.request_number
    if len(config.driver.find_elements(By.ID, requestItem)) > 0:
        print(f"Chamado {config.request_number} encontrado na fila")
    else:
        print(
            f"Chamado {config.request_number} não encontrado na fila, tentando novamente..."
        )
        time.sleep(config.looptime)
        adminFindRequestLoop()


def verifyRequestExist():
    requestItem = "list-item-" + str(config.request_number)
    if len(config.driver.find_elements(By.ID, requestItem)) > 0:
        print(f"Chamado {config.request_number} encontrado")
        return 1

    else:
        print(f"Chamado {config.request_number} não encontrado, tentando novamente...")
        time.sleep(config.looptime)
        verifyRequestExist()
        return 0


def compareRequestTextWithFile(requestId, requestText):
    print(f"Comparando descrição do chamado nº {requestId}")
    time.sleep(config.sleeptime)

    configRequest = ConfigParser()
    with open("requests.ini", "r", encoding="utf-8") as file:
        configRequest.read_file(file)
    sections = list(configRequest.keys())
    print("Texto base: " + requestText)
    for section in sections:
        if section == "DEFAULT":
            continue  # evitar reconhecer uma solução vazia no requestText
        if configRequest.get(section, "request_problem") in requestText:
            print(
                "Texto de comparação: " + configRequest.get(section, "request_problem")
            )
            config.request_number = requestId

            config.request_patrimonio = configRequest.get(section, "request_patrimonio")
            config.request_link = configRequest.get(section, "request_link")
            config.request_problem = configRequest.get(section, "request_problem")
            config.request_class_cause = configRequest.get(
                section, "request_class_cause"
            )
            config.request_class_solution = configRequest.get(
                section, "request_class_solution"
            )
            config.request_solution = configRequest.get(section, "request_solution")
            config.request_knowledge = configRequest.get(section, "request_knowledge")
            return 1
    return 0


def SelectRequestToClose():
    print(config.request_manual)
    if config.request_manual == 0:
        time.sleep(config.sleeptime)
        requestList = config.driver.find_elements(
            By.XPATH, "//div[contains(@class, 'request-id ng-binding')]"
        )
        print(f"{str(len(requestList))} requests in list")

        if len(requestList) == 0:
            print("no requests in list, trying again...")
            time.sleep(config.looptime)
            requestClose()
            return

        for r in range(len(requestList)):
            requestNumber = requestList[r].get_property("innerText")
            print(requestNumber)

            elementDescription = config.driver.find_elements(
                By.CSS_SELECTOR,
                f"#list-item-{requestNumber} > div.tableless-td.ellipsis.descricao.ng-binding.ng-hide",
            )
            requestText = elementDescription[0].get_property("innerText")
            requestText = requestText.replace("...", "")

            foundText = compareRequestTextWithFile(requestNumber, requestText)
            if foundText:
                print(f"request [{requestNumber}] is automated")
                break
            else:
                print(
                    f"request [{requestNumber}] is not automated, looking for another..."
                )

                if r == (len(requestList) - 1):
                    config.request_number = requestNumber
                    utils.setManualMode(1)
                    print(
                        f"no automated request found, opening [{requestNumber}] in manual mode..."
                    )

        print(config.page.get("admin_requestid") + config.request_number)
        config.driver.get(config.page.get("admin_requestid") + config.request_number)
        WebDriverWait(config.driver, 60).until(
            EC.presence_of_element_located((By.XPATH, xpathPageRequestReview))
        )


def setTextSolution():
    # Nome
    nameUser = config.driver.find_element(By.XPATH, xpathNameUser).text
    match (random.randint(0, 2)):
        case 0:
            nameUser = nameUser
        case 1:
            nameUser = nameUser.split()[0]
        case 2:
            if (
                len(nameUser.split()[1]) > 3
            ):  # case second part of name no has 'de', 'da', 'dos'
                nameUser = nameUser.split()[0] + " " + nameUser.split()[1]
            else:
                nameUser = nameUser.split()[0]

    if random.randint(0, 1) == 0:
        nameUser = "Sr(a) " + nameUser

    # Patrimonio~
    patrimonio = "N/A"
    try:
        patrimonioElement = WebDriverWait(config.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, xpathRequestPatrominio))
        )
        patrimonio = patrimonioElement.get_property("value")

        if patrimonio.isnumeric() == True:
            match (random.randint(0, 2)):
                case 0:
                    patrimonio = patrimonio
                case 1:
                    patrimonio = "CPE" + patrimonio
                case 2:
                    patrimonio = "DPU" + patrimonio

        if len(str(patrimonio)) < 3:
            listSemPatrimonio = ["s/n", "S/N", "Sem patrimonio", "Sem numero", "sa"]
            patrimonio = listSemPatrimonio[
                random.randint(0, (len(listSemPatrimonio) - 1))
            ]

    except Exception as e:
        print(e)

    WebDriverWait(config.driver, 60).until(
        EC.presence_of_element_located((By.XPATH, xpathSolution))
    )
    elementSolution = config.driver.find_element(By.XPATH, xpathSolution)

    # Input solution
    elementSolution.send_keys("Prezado(a): " + nameUser)
    elementSolution.send_keys(Keys.ENTER)
    elementSolution.send_keys("Patrimônio: " + patrimonio)
    elementSolution.send_keys(Keys.ENTER)

    if len(config.request_solution) < 3:
        elementSolution.send_keys(
            "Descrição de atendimento: Usuário reportou que XXXXXXX, problema resolvido, conforme havia sido solicitado."
        )
        elementSolution.send_keys(Keys.ENTER)
        elementSolution.send_keys(
            "Testes executados: Teste realizado na presença do usuário, tudo em funcionamento."
        )
        elementSolution.send_keys(Keys.ENTER)
        elementSolution.send_keys("Evidências: Segue anexo.")
        elementSolution.send_keys(Keys.ENTER)
        elementSolution.send_keys(Keys.ENTER)
        elementSolution.send_keys(
            "Sua solicitação foi atendida! Pedimos que responda nossa pesquisa de satisfação."
        )
    else:
        elementSolution.send_keys(
            "Descrição de atendimento: " + config.request_solution
        )
        elementSolution.send_keys(Keys.ENTER)
        elementSolution.send_keys(
            "Testes executados: Teste realizado na presença do usuário, tudo em funcionamento."
        )
        elementSolution.send_keys(Keys.ENTER)
        elementSolution.send_keys("Evidências: Segue anexo.")
        elementSolution.send_keys(Keys.ENTER)
        elementSolution.send_keys(Keys.ENTER)
        elementSolution.send_keys(
            "Sua solicitação foi atendida! Pedimos que responda nossa pesquisa de satisfação."
        )


def requestCapture():
    element = config.driver.find_elements(By.XPATH, f"//*[text()='Capturar ticket']")
    if element:
        utils.waitPageBlockElement()

        ActionChains(config.driver).move_to_element(element[0]).perform()
        time.sleep(config.sleeptime)
        element[0].click()

        element = WebDriverWait(config.driver, 9999).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, f"button.btn.btn-sm.btn-v3-citsmart.ng-binding")
            )
        )
        element.click()
        time.sleep(config.sleeptime)


def SetKnowledges(auto):
    element = config.driver.find_element(By.CLASS_NAME, "service-request-menu-toggle")
    element.click()
    time.sleep(config.sleeptime)

    element = config.driver.find_element(By.ID, "nav-item-service-request-knowledges")
    element.click()
    time.sleep(config.sleeptime)

    elementText = config.driver.find_elements(
        By.XPATH, f"//*[text()='Nenhum registro encontrado!']"
    )
    if len(elementText) == 0:
        utils.alert(f"Documento já anexado")
        ActionChains(config.driver).send_keys(Keys.ESCAPE).perform()
        time.sleep(config.sleeptime)
        return

    button = config.driver.find_element(
        By.XPATH, f"//button[text()='Pesquisa de Conhecimentos']"
    )
    button.click()
    time.sleep(config.sleeptime)

    if len(config.request_knowledge) <= 1:
        utils.alert(f"Modo manual - nome do documento não encontrado automaticamente")
        return

    if auto == True:
        element = config.driver.find_element(By.ID, "lookup-input-Título")
        element.send_keys(config.request_knowledge)
        time.sleep(config.sleeptime)

        button = config.driver.find_element(By.XPATH, f"//button[text()='Buscar']")
        button.click()
        time.sleep(config.sleeptime)

        element = config.driver.find_elements(By.ID, "lookup-item-0")
        if len(element) >= 1:
            element[0].click()
            time.sleep(config.sleeptime)
            print("231232132132132")
        else:
            utils.alert("Nenhum documento encontrado")
            print("999999999999999999999999999999999")
            return

        ActionChains(config.driver).send_keys(Keys.ESCAPE).perform()
        time.sleep(config.sleeptime)

        element = config.driver.find_element(
            By.CLASS_NAME, "service-request-menu-toggle"
        )
        element.click()
        time.sleep(config.sleeptime)


def requestClose():
    time.sleep(config.sleeptime)
    utils.waitPageBlockElement()
    time.sleep(config.sleeptime)

    # Suspend?
    if len(config.driver.find_elements(By.XPATH, xpathReactive)) > 0:
        config.driver.find_element(By.XPATH, xpathReactive).click()
        WebDriverWait(config.driver, 60).until(
            EC.presence_of_element_located((By.XPATH, xpathPageRequestList))
        )
        config.driver.get(config.page.get("admin_requestid") + config.request_number)

    requestCapture()

    # Button solution existis
    element = WebDriverWait(config.driver, 9999).until(
        EC.presence_of_element_located((By.ID, "radio-request-resolvida"))
    )
    ActionChains(config.driver).move_to_element(element).perform()

    WebDriverWait(config.driver, 9999).until(
        EC.invisibility_of_element_located((By.XPATH, "//div[@class='modal fade']"))
    )

    time.sleep(config.sleeptime)
    element.click()

    # Input category cause
    listClassCause = [
        "Hardware",
        "Configuration",
        "Outros",
        "Software",
        "Erro de aplicação",
        "Erro de configuração",
    ]
    config.request_class_cause = listClassCause[
        random.randint(0, (len(listClassCause) - 1))
    ]

    causeButton = WebDriverWait(config.driver, 9999).until(
        EC.element_to_be_clickable(
            (By.XPATH, '// *[ @ id = "cause"] / div[1] / span / span[2]')
        )
    )
    causeButton.click()

    config.driver.find_element(By.XPATH, '//*[@id="cause"]/input[1]').send_keys(
        config.request_class_cause
    )
    time.sleep(config.sleeptime)
    ActionChains(config.driver).send_keys(Keys.RETURN).perform()

    # Input category solution
    listClassSolution = [
        "Ajuste na configuração do aplicativo",
        "Ajustes de configurações do sistema",
        "Hardware",
        "Software",
        "Ajuste de configuração de software",
    ]
    config.request_class_solution = listClassSolution[
        random.randint(0, (len(listClassSolution) - 1))
    ]

    config.driver.find_element(
        By.XPATH, '//*[@id="solution-category"]/div[1]/span/span[2]'
    ).click()

    config.driver.find_element(
        By.XPATH, '//*[@id="solution-category"]/input[1]'
    ).send_keys(config.request_class_solution)
    time.sleep(config.sleeptime)
    ActionChains(config.driver).send_keys(Keys.RETURN).perform()

    elementRequestNumber = config.driver.find_element(
        By.XPATH,
        '//*[@id="service-request-view"]/div/div/div/div[1]/div/ul/li[1]/div[1]/div[2]/div[2]',
    )
    requestNumber = elementRequestNumber.get_property("innerText")
    elementDescription = config.driver.find_elements(
        By.XPATH,
        '//*[@id="service-request-view"]/div/div/div/div[2]/div/div/div[3]/div[2]/div[1]/div/fieldset/div[2]/div/div/div',
    )
    requestText = elementDescription[0].get_property("innerText")
    requestText = requestText.replace("\n", "")
    print(requestText)
    compareRequestTextWithFile(requestNumber, requestText)
    setTextSolution()

    if config.request_manual == 1:  # Manual
        SetKnowledges(False)

    else:  # Automatico
        SetKnowledges(True)
        if config.waitConfirmClose == 0:
            WebDriverWait(config.driver, 9999).until(
                EC.invisibility_of_element_located(
                    (By.XPATH, "//div[@class='modal fade']")
                )
            )

            element = WebDriverWait(config.driver, 9999).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '// *[ @ id = "request-save-submit"]')
                )
            )
            element.click()

    WebDriverWait(config.driver, 9999).until(
        EC.invisibility_of_element_located(
            (
                By.XPATH,
                '// *[ @ id = "request-save-submit"]',
            )
        )
    )
    time.sleep(config.sleeptime)
    print("Chamado nº " + config.request_number + " fechado")
