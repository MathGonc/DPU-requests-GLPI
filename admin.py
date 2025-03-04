import random
import os
import re  # To extract number request
from configparser import ConfigParser


from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException, NoSuchElementException

import time
import config
import menu
import cookies
import utils
import user
from driver import driver

xpathSolution = "/html/body/div[3]/div/div[2]/div/div[1]/div/form/div/div/div/div/div/div[2]/div/div/div[3]/div[2]/div[6]/div/fieldset/div[4]/div[2]/div/div/citsmart-trix-editor/div/trix-editor"
xpathNameUser = '//*[@id="service-request-view"]/div/div/div/div[2]/div/div/div[3]/div[1]/div[1]/div/fieldset/div[1]/div[1]/div/div[2]'
xpathRequestCaptureTicket = '//*[@id="service-request-view"]/div/div/div/div[1]/div/ul/li[4]/div[1]/div[2]/div[2]/span/a'
xpathRequestLoading = (
    '//*[@id="divCorpoJanelaAguarde_JANELA_AGUARDE_MENU"]/table/tbody/tr/td'
)

xpathPageRequestList = '//*[@id="service-request-incident-container"]/div[1]'
xpathPageRequestReview = '//*[@id="service-request-view"]/div/div/div/div[1]/div'


def compareRequestTextWithFile(requestId, requestText):
    print(f"Comparando descrição do chamado nº {requestId}")
    time.sleep(config.sleeptime)

    configRequest = ConfigParser()
    with open("requests.ini", "r", encoding="utf-8") as file:
        configRequest.read_file(file)
    sections = list(configRequest.keys())
    print("\nTexto encontrado no chamado:\n" + requestText + "\n\n")
    for section in sections:
        if section == "DEFAULT":
            continue  # evitar reconhecer uma solução vazia no requestText
        if configRequest.get(section, "request_problem") in requestText:
            print(
                "\nTexto no banco de dados encontrado:\n"
                + configRequest.get(section, "request_problem")
                + "\n\n"
            )
            config.request_number = requestId

            config.request_patrimonio = configRequest.get(section, "request_patrimonio")
            config.request_link = configRequest.get(section, "request_link")
            config.request_problem = configRequest.get(section, "request_problem")
            config.request_category = configRequest.get(section, "request_category")
            config.request_class_solution = configRequest.get(
                section, "request_class_solution"
            )
            config.request_solution = configRequest.get(section, "request_solution")
            config.request_knowledge = configRequest.get(section, "request_knowledge")
            return 1
    return 0


def SelectRequestToClose():

    # element = WebDriverWait(driver, 99999).until(  # Button to open request List
    #     EC.element_to_be_clickable(
    #         (
    #             By.CSS_SELECTOR,
    #             "#tabspanel > li:nth-child(2) > a",
    #         )
    #     )
    # )
    # element.click()
    # WebDriverWait(driver, 99999).until(
    #     EC.presence_of_element_located(
    #         (
    #             By.XPATH,
    #             "//div[@data-itemtype='Reminder']",
    #         )
    #     )
    # )  # Last Element of my requests page loaded

    # delete tickets awaiting validation, so they don't count towards pending tickets
    #     driver.execute_script(
    #         """
    #     var elements = document.evaluate(
    #         '//div[contains(@data-params, "survey")]',
    #         document,
    #         null,
    #         XPathResult.UNORDERED_NODE_SNAPSHOT_TYPE,
    #         null
    #     );
    #     for (var i = 0; i < elements.snapshotLength; i++) {
    #         elements.snapshotItem(i).remove();
    #     }
    # """
    #     )

    if config.request_manual == 0:
        print("Procurando chamados...")
        # *** TO DO: Insert loop
        element = WebDriverWait(driver, 99999).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//*[contains(@href, '/front/ticket.form.php?id=')]",
                )
            )
        )

        elementRequests = driver.find_elements(
            By.XPATH,
            "//*[contains(@href, '/front/ticket.form.php?id=')]",
        )
        print(f"Chamados encontrados: {len(elementRequests)}")

        # FIX ITTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT
        for r in range(len(elementRequests)):
            elementNumberRequest = elementRequests[r].get_property("search")
            print(f"Debug: {elementNumberRequest}")
            requestNumber = re.search(r"id=(\d+)", elementNumberRequest).group(
                1
            )  # Example: Extract "479" from "?id=479&forcetab=Ticket$2"
            print(f"\nAnalisando chamado: {requestNumber}")

            ActionChains(driver).move_to_element(
                elementRequests[r]
            ).perform()  # Move to element for show "qtip-content" class

            elementDescription = WebDriverWait(driver, 99999).until(
                EC.presence_of_element_located(
                    (
                        By.CLASS_NAME,
                        "qtip-content",
                    )
                )
            )

            requestText = elementDescription.get_property("textContent")
            # print(f"Debug:\n{requestText}")

            foundText = compareRequestTextWithFile(requestNumber, requestText)
            if foundText:
                print(f"request [{requestNumber}] is automated")
                break
            else:
                print(
                    f"request [{requestNumber}] is not automated, looking for another..."
                )

                if r == (len(elementRequests) - 1):
                    config.request_number = requestNumber
                    utils.setManualMode(1)
                    print(
                        f"no automated request found, opening [{requestNumber}] in manual mode..."
                    )

        print(config.page.get("admin_requestid") + config.request_number)
        driver.get(
            f"https://suporte.dpu.def.br/front/ticket.form.php?id={config.request_number}&forcetab=Ticket$2"
        )

        # WebDriverWait(driver, 60).until(
        #     EC.presence_of_element_located((By.XPATH, xpathPageRequestReview))
        # )


def setStatus():

    # Click in status box
    WebDriverWait(driver, 99999).until(
        EC.element_to_be_clickable(
            (
                By.CSS_SELECTOR,
                "#item-main > div > div:nth-child(4) > div > span",
            )
        )
    ).click()

    time.sleep(1)

    # Click in solution
    WebDriverWait(driver, 99999).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                f"//*[text()='Solucionado']",
            )
        )
    ).click()

    WebDriverWait(driver, 99999).until(
        EC.element_to_be_clickable(
            (
                By.CSS_SELECTOR,
                f"#page > div > div > div.col > div.navigationheader.justify-content-sm-between > h3",
            )
        )
    ).click()


def setLocation():
    element = WebDriverWait(driver, 99999).until(
        EC.element_to_be_clickable(
            (
                By.CSS_SELECTOR,
                "#item-main > div > div:nth-child(8) > div > div > span.select2.select2-container.select2-container--default > span.selection > span",
            )
        )
    )
    element.click()
    actions = ActionChains(driver)
    actions.send_keys(config.city).perform()
    time.sleep(1)
    actions.send_keys(Keys.ENTER).perform()

    WebDriverWait(driver, 99999).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//button[contains(@title, 'Salvar')]",
            )
        )
    ).click()


def setTextSolution():
    # User name
    element = WebDriverWait(driver, 99999).until(
        EC.presence_of_element_located(
            (
                By.CSS_SELECTOR,
                "#actors > div > div:nth-child(1) > div > span > span.selection > span > ul > li.select2-selection__choice > span.actor_entry > span.actor_text",
            )
        )
    )
    nameUser = element.get_property("innerHTML")
    print(f"nameUser: {nameUser}")

    # Solution
    WebDriverWait(driver, 99999).until(
        EC.presence_of_element_located(
            (
                By.CSS_SELECTOR,
                "#itil-footer > div > div.col.col-lg-8.ps-3.timeline-buttons.d-flex > div.btn-group.me-2.main-actions > button.btn.btn-primary.dropdown-toggle.dropdown-toggle-split.mb-2",
            )
        )
    ).click()  # Expand menu solution

    WebDriverWait(driver, 99999).until(
        EC.presence_of_element_located(
            (
                By.CSS_SELECTOR,
                "#itil-footer > div > div.col.col-lg-8.ps-3.timeline-buttons.d-flex > div.btn-group.me-2.main-actions > ul > li:nth-child(2) > a > span",
            )
        )
    ).click()

    time.sleep(1)
    WebDriverWait(driver, 99999).until(
        EC.element_to_be_clickable(
            (
                By.CSS_SELECTOR,
                "#new-ITILSolution-block > div > div.col > div > div > div.clearfix",
            )
        )
    ).click()  # Box solution (for dont need to enter in iframe)
    ActionChains(driver).send_keys(Keys.TAB).send_keys(Keys.TAB).perform()
    # driver.switch_to.frame(iframeText)

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

    # Patrimonio
    patrimonio = "N/A"
    try:
        # patrimonioElement = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located(
        #         (
        #             By.CSS_SELECTOR,
        #             "#itil-object-container > div.row.d-flex.flex-column.alin-items-stretch.itil-object > div.itil-left-side.col-12.col-lg-8.order-last.order-lg-first.pt-2.pe-2.pe-lg-4.d-flex.flex-column-reverse.border-top.border-4 > div > div.timeline-item.mb-3.ITILContent > div > div.col-12.col-sm > div",
        #         )
        #     )
        # )

        # patrimonioText = patrimonioElement.get_property("outerText")
        # print(patrimonioText)
        # patrimonio = patrimonioText.split("(Etiqueta branca) : ", 1)[1].strip()
        # print(patrimonio)

        # # patrimonio = patrimonioElement.get_property("value")
        # config.request_patrimonio = patrimonio
        # print("Patrimonio: " + patrimonio)

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

    # WebDriverWait(driver, 60).until(
    #     EC.presence_of_element_located((By.XPATH, xpathSolution))
    # )
    # actions = driver.find_element(By.CLASS_NAME, "tox-edit-area__iframe")

    # Input solution
    actions = ActionChains(driver)
    actions.send_keys("Usuário(a): " + nameUser)
    actions.send_keys(Keys.ENTER)

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
        actions.send_keys("Ações realizadas: " + textSolution)
    else:
        actions.send_keys("Ações realizadas: " + config.request_solution)
    actions.send_keys(Keys.ENTER)

    actions.send_keys("Patrimônio: " + patrimonio)
    actions.send_keys(Keys.ENTER)

    actions.send_keys(
        "Testes executados: Teste realizado na presença do usuário, tudo em funcionamento."
    )
    actions.send_keys(Keys.ENTER)
    actions.send_keys("Evidência(s): Segue anexo.")
    actions.send_keys(Keys.ENTER)
    actions.send_keys(Keys.ENTER)
    actions.send_keys(
        "Sua solicitação foi atendida! A sua opinião é muito importante, pedimos que responda nossa pesquisa de satisfação."
    )

    actions.perform()
    # driver.switch_to.default_content()  # exit iframe


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

    # usar try não está funcionando, o except não é chamado
    time.sleep(3)
    element = driver.find_elements(
        By.XPATH, "//*[text()='Nenhum registro encontrado!']"
    )
    if element:
        utils.alert("Nenhum patrimonio encontrado")
    else:
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

    element = driver.find_elements(
        By.XPATH,
        "//a[contains(@title, 'Base de Conhecimento')]//span[@class='badge' and text()='1']",
    )
    if element:
        print("Knowledge already inserted")
        return

    element = WebDriverWait(driver, 99999).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#tabspanel > li:nth-child(4) > a")
        )
    )
    element.click()

    while True:
        element = WebDriverWait(driver, 99999).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[contains(@id, 'select2-dropdown_knowbaseitems_id')]")
            )
        )
        element.click()

        elementInput = WebDriverWait(driver, 99999).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "body > span > span > span.select2-search.select2-search--dropdown > input",
                )
            )
        )

        if config.request_knowledge:
            elementInput.send_keys(config.request_knowledge)
            time.sleep(1)

            # WebDriverWait(driver, 99999).until(  # Wait search
            #     EC.invisibility_of_element(
            #         (By.XPATH, f"//*[contains(text()='Searching...')]")
            #     )
            # )
            # time.sleep(1)

            element = driver.find_elements(
                By.XPATH, "//li[contains(text(), 'No results found')]"
            )
            if element:
                print("Nenhum conhecimento encontrado, aguardando para continuar...")
                element = WebDriverWait(driver, 99999).until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "//a[contains(@title, 'Base de Conhecimento')]//span[@class='badge' and text()='1']",
                        )
                    )
                )
            else:
                elementInput.send_keys(Keys.ENTER)
                # time.sleep(1)
                # element = driver.find_elements(
                #     By.XPATH,
                #     "//*[contains(@id, 'select2-dropdown_knowbaseitems_id') and not(@title='-----')]",
                # )
                # if element:
                #     print("ERROR: Knowledge dont insert...")
                # else:
                #     print("Knowledge sucessful insert")

                element = WebDriverWait(driver, 99999).until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            "//input[contains(@value, 'Adicionar')]",
                        )
                    )
                )
                element.click()

                element = WebDriverWait(driver, 99999).until(
                    EC.invisibility_of_element(
                        (
                            By.XPATH,
                            "//input[contains(@value, 'Adicionar')]",
                        )
                    )
                )

                time.sleep(1)
                element = driver.find_elements(
                    By.XPATH,
                    "//div[contains(text(), 'Item adicionado com sucesso: Item da base de conhecimento')]",
                )

                if element:
                    print("Knowledge sucessful")
                else:
                    element = driver.find_elements(
                        By.XPATH, "//a[contains(@href, 'Return to previous page')]"
                    )
                    if element:
                        print(
                            "ERROR: Button 'Adicionar' has been pressed with input field empty, manual mode..."
                        )
                        element[0].click()
                        continue

        else:
            print("Nenhum conhecimento vinculado, aguardando para continuar...")

        element = WebDriverWait(driver, 99999).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//a[contains(@title, 'Base de Conhecimento')]//span[@class='badge' and text()='1']",
                )
            )
        )

        element = WebDriverWait(driver, 99999).until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,
                    "#tabspanel > li:nth-child(1) > a",
                )
            )
        )
        element.click()
        return


def requestClose():
    # time.sleep(config.sleeptime)
    # if utils.verifyPageErrorExist() == True:
    #     return requestClose()
    # utils.waitPageBlockElement()
    # time.sleep(config.sleeptime)

    if config.request_manual == 1:  # Get request number to link in manual mode
        WebDriverWait(driver, 99999).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "#linked_tickets > div > input[type=hidden]",
                )
            )
        )
        config.request_number = driver.find_element(
            By.CSS_SELECTOR,
            "#linked_tickets > div > input[type=hidden]",
        ).get_property("value")
        print("config.request_number: ", config.request_number)

    # Suspend?
    # xpathReactive = '//*[@id="request-reactivate"]'
    # if len(driver.find_elements(By.XPATH, xpathReactive)) > 0:

    #     driver.find_element(By.XPATH, xpathReactive).click()
    #     WebDriverWait(driver, 60).until(
    #         EC.presence_of_element_located((By.XPATH, xpathPageRequestList))
    #     )

    #     driver.get(config.page.get("admin_requestid") + config.request_number)

    # requestCapture()

    elementDescription = driver.find_elements(
        By.CSS_SELECTOR,
        "#itil-object-container > div.row.d-flex.flex-column.alin-items-stretch.itil-object > div.itil-left-side.col-12.col-lg-8.order-last.order-lg-first.pt-2.pe-2.pe-lg-4.d-flex.flex-column-reverse.border-top.border-4 > div > div.timeline-item.mb-3.ITILContent > div > div.col-12.col-sm > div",
    )
    if elementDescription:
        requestText = elementDescription[0].get_property("innerText")
        requestText = requestText.replace("\n", "")
        print(requestText)
        compareRequestTextWithFile(config.request_number, requestText)
    else:
        print("Texto para comparação não encontrado, inserindo texto genérico...")

    # setStatus() # Dont need set solution, because button add solution already set this status
    SetKnowledges(1)
    setLocation()
    setTextSolution()

    print("config.request_manual: ", config.request_manual)
    print("config.waitConfirmClose: ", config.waitConfirmClose)
    if config.request_manual == 1:  # TEMP
        if config.waitConfirmClose == 1:  # TEMP
            WebDriverWait(driver, 99999).until(  # FIX ITTTTT
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//button[@name='add']",
                    )
                )
            ).click()

            WebDriverWait(driver, 99999).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//div[contains(text(), 'Item adicionado com sucesso')]",
                    )
                )
            )

            # Click in status box
            WebDriverWait(driver, 99999).until(
                EC.element_to_be_clickable(
                    (
                        By.CSS_SELECTOR,
                        "#item-main > div > div:nth-child(4) > div > span",
                    )
                )
            ).click()

            time.sleep(1)

            # Click in solution
            WebDriverWait(driver, 99999).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        f"//*[text()='Fechado']",
                    )
                )
            ).click()

            WebDriverWait(driver, 99999).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//button[contains(@title, 'Salvar')]",
                    )
                )
            ).click()

            WebDriverWait(driver, 99999).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//div[contains(text(), 'Item atualizado com sucesso')]",
                    )
                )
            )

    print("Chamado nº " + config.request_number + " fechado")
    time.sleep(99999)
