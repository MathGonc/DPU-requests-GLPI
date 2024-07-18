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
from driver import driver

xpathSolution = "/html/body/div[3]/div/div[2]/div/div[1]/div/form/div/div/div/div/div/div[2]/div/div/div[3]/div[2]/div[6]/div/fieldset/div[4]/div[2]/div/div/citsmart-trix-editor/div/trix-editor"
xpathNameUser = '//*[@id="service-request-view"]/div/div/div/div[2]/div/div/div[3]/div[1]/div[1]/div/fieldset/div[1]/div[1]/div/div[2]'
xpathRequestCaptureTicket = '//*[@id="service-request-view"]/div/div/div/div[1]/div/ul/li[4]/div[1]/div[2]/div[2]/span/a'
xpathRequestLoading = (
    '//*[@id="divCorpoJanelaAguarde_JANELA_AGUARDE_MENU"]/table/tbody/tr/td'
)

xpathPageRequestList = '//*[@id="service-request-incident-container"]/div[1]'
xpathPageRequestReview = '//*[@id="service-request-view"]/div/div/div/div[1]/div'


def adminLogin():
    print("adminLogin", adminLogin)
    cookies.loadCookie(cookies.cookieAdminFile)
    driver.get(config.page["admin"])
    WebDriverWait(driver, 99999).until(
        EC.presence_of_element_located((By.NAME, "list-item"))
    )


def adminFindRequestLoop():
    # driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div/div[1]/div/form/div/div[2]/div[1]/div[2]/button[2]/i').click() #click in refresh and wait

    requestItem = "list-item-" + config.request_number
    if len(driver.find_elements(By.ID, requestItem)) > 0:
        print(f"Chamado {config.request_number} encontrado na fila")
    else:
        print(
            f"Chamado {config.request_number} não encontrado na fila, tentando novamente..."
        )
        time.sleep(config.looptime)
        adminFindRequestLoop()


def verifyRequestExist():
    requestItem = "list-item-" + str(config.request_number)
    if len(driver.find_elements(By.ID, requestItem)) > 0:
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
    print("\nTexto encontrado no site:\n" + requestText + "\n\n")
    for section in sections:
        if section == "DEFAULT":
            continue  # evitar reconhecer uma solução vazia no requestText
        if requestText in configRequest.get(section, "request_problem"):
            print(
                "\nTexto base para comparação:\n"
                + configRequest.get(section, "request_problem")
                + "\n\n"
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
    if config.request_manual == 0:
        time.sleep(config.sleeptime)
        requestList = driver.find_elements(
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

            elementDescription = driver.find_elements(
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
        driver.get(config.page.get("admin_requestid") + config.request_number)
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, xpathPageRequestReview))
        )


def setTextSolution():
    # Nome
    nameUser = driver.find_element(By.XPATH, xpathNameUser).text
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
        patrimonioElement = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "/html/body/div[3]/div/div[2]/div/div[1]/div/form/div/div/div/div/div/div[2]/div/div/div[3]/div[2]/div[3]/div/fieldset/div/div/div[3]/div[2]/div/div/input",
                )
            )
        )
        patrimonio = patrimonioElement.get_property("value")
        config.request_patrimonio = patrimonioElement.get_property("value")
        print("Patrimonio: " + patrimonio)

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

    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, xpathSolution))
    )
    elementSolution = driver.find_element(By.XPATH, xpathSolution)

    # Input solution
    elementSolution.send_keys("Prezado(a): " + nameUser)
    elementSolution.send_keys(Keys.ENTER)
    elementSolution.send_keys("Patrimônio: " + patrimonio)
    elementSolution.send_keys(Keys.ENTER)

    textSolutionPart1 = random.choice(
        ["reportou", "comunicou", "informou", "pediu", "solicitou"]
    )
    textSolutionPart2 = random.choice(["problema", "chamado", "ticket"])
    textSolutionPart3 = random.choice(["resolvido", "solucionado"])
    textSolutionPart4 = random.choice(["conforme havia sido", "como foi"])
    textSolutionPart5 = random.choice(["pedido", "solicitado"])
    textSolution = (
        "Usuário "
        + textSolutionPart1
        + " XXXXXXX, "
        + textSolutionPart2
        + " "
        + textSolutionPart3
        + ", "
        + textSolutionPart4
        + " "
        + textSolutionPart5
        + "."
    )
    if len(config.request_solution) < 3:
        elementSolution.send_keys("Descrição de atendimento: " + textSolution)
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
    element = driver.find_elements(By.XPATH, f"//*[text()='Capturar ticket']")
    if element:
        utils.waitPageBlockElement()

        ActionChains(driver).move_to_element(element[0]).perform()
        time.sleep(config.sleeptime)
        element[0].click()

        element = WebDriverWait(driver, 99999).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, f"button.btn.btn-sm.btn-v3-citsmart.ng-binding")
            )
        )
        element.click()
        time.sleep(config.sleeptime)


def SetIcRelated():
    element = driver.find_element(By.ID, "nav-item-service-request-configuration-item")
    element.click()

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.ID, "modal-request-configuration-item-pesquisar")
        )
    )
    element.click()

    driver.switch_to.frame("iframeModal")  # enter iframe
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "filtroIdentificacao"))
    )
    element.send_keys(config.request_patrimonio)

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "btnpesquisa"))
    )
    element.click()

    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, f"//*[text()='Nenhum registro encontrado!']")
            )
        )
        utils.alert("Nenhum patrimonio encontrado")
    except:
        utils.alert("Patrimonio encontrado")
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, f"//a[text()='Selecionar						']")
            )
        )
        element.click()
        time.sleep(config.sleeptime)
        driver.switch_to.default_content()  # exit iframe
        ActionChains(driver).send_keys(Keys.ESCAPE).perform()

    # Wait for the main menu to be clickable to continue
    element = WebDriverWait(driver, 99999).until(
        EC.element_to_be_clickable((By.ID, "cit--header-menu-toogle-link"))
    )


def SetKnowledges(auto):

    element = driver.find_element(By.ID, "nav-item-service-request-knowledges")
    element.click()
    time.sleep(config.sleeptime)

    elementText = driver.find_elements(
        By.XPATH, f"//*[text()='Nenhum registro encontrado!']"
    )
    if len(elementText) == 0:
        utils.alert(f"Documento já anexado")
        ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        time.sleep(config.sleeptime)
        return

    button = driver.find_element(
        By.XPATH, f"//button[text()='Pesquisa de Conhecimentos']"
    )
    button.click()
    time.sleep(config.sleeptime)

    if len(config.request_knowledge) <= 1:
        utils.alert(f"Modo manual - nome do documento não encontrado automaticamente")
        return

    if auto == True:
        element = driver.find_element(By.ID, "lookup-input-Título")
        element.send_keys(config.request_knowledge)
        time.sleep(config.sleeptime)

        button = driver.find_element(By.XPATH, f"//button[text()='Buscar']")
        button.click()
        time.sleep(config.sleeptime)

        element = driver.find_elements(By.ID, "lookup-item-0")
        if len(element) >= 1:
            element[0].click()
            time.sleep(config.sleeptime)
            print("231232132132132")
        else:
            utils.alert("Nenhum documento encontrado")
            print("999999999999999999999999999999999")
            return

        ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        time.sleep(config.sleeptime)
        toggleServiceRequestMenu()


def toggleServiceRequestMenu():
    element = driver.find_element(By.CLASS_NAME, "service-request-menu-toggle")
    element.click()


def requestClose():
    time.sleep(config.sleeptime)
    if utils.verifyPageErrorExist() == True:
        return requestClose()
    utils.waitPageBlockElement()
    time.sleep(config.sleeptime)

    if config.request_manual == 1:  # Get request number to link in manual mode
        WebDriverWait(driver, 99999).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "#service-request-view > div > div > div > div:nth-child(1) > div > ul > li:nth-child(1) > div.info.pull-left > div:nth-child(2) > div.description.ng-binding",
                )
            )
        )
        config.request_number = driver.find_element(
            By.CSS_SELECTOR,
            "#service-request-view > div > div > div > div:nth-child(1) > div > ul > li:nth-child(1) > div.info.pull-left > div:nth-child(2) > div.description.ng-binding",
        ).get_property("innerText")
        print("config.request_number: ", config.request_number)
        time.sleep(config.sleeptime)

    # Suspend?
    xpathReactive = '//*[@id="request-reactivate"]'
    if len(driver.find_elements(By.XPATH, xpathReactive)) > 0:

        driver.find_element(By.XPATH, xpathReactive).click()
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, xpathPageRequestList))
        )

        driver.get(config.page.get("admin_requestid") + config.request_number)

    requestCapture()

    # Button solution existis
    element = WebDriverWait(driver, 99999).until(
        EC.presence_of_element_located((By.ID, "radio-request-resolvida"))
    )
    ActionChains(driver).move_to_element(element).perform()

    WebDriverWait(driver, 99999).until(
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

    causeButton = WebDriverWait(driver, 99999).until(
        EC.element_to_be_clickable(
            (By.XPATH, '// *[ @ id = "cause"] / div[1] / span / span[2]')
        )
    )
    causeButton.click()

    driver.find_element(By.XPATH, '//*[@id="cause"]/input[1]').send_keys(
        config.request_class_cause
    )
    time.sleep(config.sleeptime)
    ActionChains(driver).send_keys(Keys.RETURN).perform()

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

    driver.find_element(
        By.XPATH, '//*[@id="solution-category"]/div[1]/span/span[2]'
    ).click()

    driver.find_element(By.XPATH, '//*[@id="solution-category"]/input[1]').send_keys(
        config.request_class_solution
    )
    time.sleep(config.sleeptime)
    ActionChains(driver).send_keys(Keys.RETURN).perform()

    elementRequestNumber = driver.find_element(
        By.XPATH,
        '//*[@id="service-request-view"]/div/div/div/div[1]/div/ul/li[1]/div[1]/div[2]/div[2]',
    )
    requestNumber = elementRequestNumber.get_property("innerText")
    elementDescription = driver.find_elements(
        By.XPATH,
        '//*[@id="service-request-view"]/div/div/div/div[2]/div/div/div[3]/div[2]/div[1]/div/fieldset/div[2]/div/div/div',
    )
    if elementDescription:
        requestText = elementDescription[0].get_property("innerText")
        requestText = requestText.replace("\n", "")
        print(requestText)
        compareRequestTextWithFile(requestNumber, requestText)
    else:
        print("Texto para comparação não encontrado, inserindo texto genérico...")

    setTextSolution()

    toggleServiceRequestMenu()
    time.sleep(config.sleeptime)
    SetIcRelated()
    time.sleep(config.sleeptime)

    if config.request_manual == 1:  # Manual
        SetKnowledges(False)

    else:  # Automatico
        SetKnowledges(True)
        if config.waitConfirmClose == 0:
            WebDriverWait(driver, 99999).until(
                EC.invisibility_of_element_located(
                    (By.XPATH, "//div[@class='modal fade']")
                )
            )

            element = WebDriverWait(driver, 99999).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '// *[ @ id = "request-save-submit"]')
                )
            )
            element.click()

    WebDriverWait(driver, 99999).until(
        EC.invisibility_of_element_located(
            (
                By.XPATH,
                '// *[ @ id = "request-save-submit"]',
            )
        )
    )
    time.sleep(config.sleeptime)
    print("Chamado nº " + config.request_number + " fechado")
