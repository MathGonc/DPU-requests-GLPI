import random
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import config
import menu
import cookies

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


def admin_login():
    cookies.loadCookie(cookies.cookieAdminFile)
    # config.driver.get(config.page.get('login'))
    config.driver.get(config.page.get("admin"))
    # refresh to admin screen
    WebDriverWait(config.driver, 60).until(
        EC.presence_of_element_located((By.XPATH, xpathPageRequestList))
    )


def admin_findRequestLoop():
    # config.driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div/div[1]/div/form/div/div[2]/div[1]/div[2]/button[2]/i').click() #click in refresh and wait

    requestItem = "list-item-" + config.request_number
    if len(config.driver.find_elements(By.ID, requestItem)) > 0:
        print("Chamado " + config.request_number + " encontrado na fila")
    else:
        print(
            "Chamado "
            + config.request_number
            + " não encontrado na fila, tentando novamente..."
        )
        time.sleep(config.looptime)
        admin_findRequestLoop()


def verifyRequestExist():
    requestItem = "list-item-" + str(config.request_number)
    if len(config.driver.find_elements(By.ID, requestItem)) > 0:
        print("Chamado " + config.request_number + " encontrado")

    else:
        print(
            "Chamado "
            + config.request_number
            + " não encontrado,  tentando novamente..."
        )
        time.sleep(config.looptime)
        verifyRequestExist()


def verifyRequestIsAuto(requestId):
    print("Verificando chamado nº" + requestId)
    count = 0
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

            requestText = config.driver.find_element(
                By.XPATH, '//*[@id="list-item-' + requestId + '"]/div[10]'
            ).get_property("innerText")
            # requestText.encode('utf8')
            # print("innerText: " + requestText)
            requestText = requestText.replace("...", "")  # replace ... in final text
            if requestText in request[3]:  # line 4
                config.request_problem = request[3]
                config.request_class_cause = request[4]
                config.request_class_solution = request[5]
                config.request_solution = request[6]
                return 1
    return 0


def closeRequest():
    if config.request_manual == 0:
        time.sleep(config.sleeptime)
        requestList = config.driver.find_elements(
            By.XPATH, "//div[contains(@class, 'request-id ng-binding')]"
        )
        print(str(len(requestList)) + " requests in list")

        if len(requestList) == 0:
            print("no requests in list, trying again...")
            time.sleep(config.looptime)
            return closeRequest()

        for r in range(len(requestList)):
            requestNumber = requestList[r].get_property("innerText")
            print(requestNumber)
            if verifyRequestIsAuto(requestNumber) == 1:
                config.request_number = requestNumber
                print("request " + requestNumber + " is automated")
                break
            else:
                print(
                    "request "
                    + requestNumber
                    + " is not automated, looking for another..."
                )

                if r == (len(requestList) - 1):
                    config.request_number = requestNumber
                    config.request_manual = 1
                    print(
                        "no automated request found, opening ["
                        + requestNumber
                        + "] in manual mode..."
                    )

    print(config.page.get("admin_requestid") + config.request_number)
    config.driver.get(config.page.get("admin_requestid") + config.request_number)
    WebDriverWait(config.driver, 60).until(
        EC.presence_of_element_located((By.XPATH, xpathPageRequestReview))
    )

    # Suspend?
    if len(config.driver.find_elements(By.XPATH, xpathReactive)) > 0:
        config.driver.find_element(By.XPATH, xpathReactive).click()
        WebDriverWait(config.driver, 60).until(
            EC.presence_of_element_located((By.XPATH, xpathPageRequestList))
        )
        config.driver.get(config.page.get("admin_requestid") + config.request_number)

    """
    # capture request and confirm
    if len(config.driver.find_elements(By.XPATH,xpathRequestCaptureTicket)) > 0:
        time.sleep(config.sleeptime)
        config.driver.find_element(By.XPATH,xpathRequestCaptureTicket).click()

        WebDriverWait(config.driver, 60).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[3]/button[1]')))
        if len(config.driver.find_elements(By.XPATH, '/html/body/div[1]/div/div/div[3]/button[1]')) > 0:
            config.driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[3]/button[1]').click()
    else:
        print('chamado já capturado')
    """

    # Button solution existis
    WebDriverWait(config.driver, 60).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="radio-request-resolvida"]'))
    )
    time.sleep(config.sleeptime)
    config.driver.find_element(By.XPATH, '//*[@id="radio-request-resolvida"]').click()

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

    WebDriverWait(config.driver, 60).until(
        EC.invisibility_of_element_located((By.CLASS_NAME, "loading-neuro"))
    )
    print("Field insert patrimonio loaded")

    # Patrimonio
    WebDriverWait(config.driver, 60).until(
        EC.presence_of_element_located((By.XPATH, xpathRequestPatrominio))
    )
    patrimonio = config.driver.find_element(
        By.XPATH, xpathRequestPatrominio
    ).get_property("value")

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
        patrimonio = listSemPatrimonio[random.randint(0, (len(listSemPatrimonio) - 1))]

    WebDriverWait(config.driver, 60).until(
        EC.presence_of_element_located((By.XPATH, xpathSolution))
    )
    elementSolution = config.driver.find_element(By.XPATH, xpathSolution)

    # Input category cause
    listClassCause = [
        "Hardware",
        "Configuration",
        "Outros",
        "Software",
        "Erro de aplicação",
        "Erro de configuação",
    ]
    config.request_class_cause = listClassCause[
        random.randint(0, (len(listClassCause) - 1))
    ]

    config.driver.find_element(
        By.XPATH, '// *[ @ id = "cause"] / div[1] / span / span[2]'
    ).click()
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

    # Input solution
    elementSolution.send_keys("Prezado(a): " + nameUser)
    elementSolution.send_keys(Keys.ENTER)
    elementSolution.send_keys("Patrimônio: " + patrimonio)
    elementSolution.send_keys(Keys.ENTER)

    # Manual
    if config.request_manual == 1:
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

        try:
            wait = WebDriverWait(config.driver, 99999)
            wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//*[@id="service-request-incident-container"]/div[1]/div[1]',
                    )
                )
            )  # tickets list
        finally:
            time.sleep(config.sleeptime)

    # Automatico
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

        config.driver.find_element(
            By.XPATH, '// *[ @ id = "request-save-submit"]'
        ).click()  # gravar e enviar
        time.sleep(config.sleeptime)

        # capture request and confirm
        if (
            len(
                config.driver.find_elements(
                    By.XPATH, "/html/body/div[1]/div/div/div[3]/button[1]"
                )
            )
            > 0
        ):
            config.driver.find_element(
                By.XPATH, "/html/body/div[1]/div/div/div[3]/button[1]"
            ).click()
            time.sleep(config.sleeptime)

    print("Chamado nº " + config.request_number + " fechado")
