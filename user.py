from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import config
import utils
import cookies
import random
import logintxt
from driver import driver


def rateRequest():
    login()
    loadPresetUserInfo()
    driver.get(config.page.get("rate"))

    element = WebDriverWait(driver, 99999).until(
        EC.presence_of_element_located((By.ID, "idStatusMinhasSolicitacoes"))
    )
    time.sleep(config.sleeptime)
    element.click()
    element.send_keys("Todos" + Keys.ENTER)
    time.sleep(config.sleeptime)

    button = driver.find_element(
        By.CSS_SELECTOR,
        f"#formMinhasSolicitacoes > div.row > div > div.col-md-1 > button",
    )
    time.sleep(config.sleeptime)
    button.click()
    time.sleep(config.sleeptime)

    element = driver.find_elements(By.XPATH, f"//i[text()='thumbs_up_down']")
    utils.alert(f"{len(element)} chamados a serem avaliados")

    time.sleep(9999)


def OpenRequest():
    loadPresetUserInfo()
    login(0)
    setPageRequest()
    setRequestInfo()
    userLogout()


def login(admin=0):

    if config.saveLoginTxt == 1:
        driver.refresh()
        if admin == 1:
            logintxt.loadUserPass("ADMIN")
            logintxt.inputLogin()
            driver.get(config.page["admin"])
        elif len(config.userName) > 0:
            logintxt.loadUserPass(config.userName)
            logintxt.inputLogin()
            driver.get(config.page.get("home"))
        else:
            logintxt.inputUserPass()
    else:  # Load via cookies
        if admin == 1:
            cookies.loadCookie(cookies.cookieAdminFile)
            driver.get(config.page["admin"])
        else:
            if len(config.userName) > 0:
                cookies.loadCookie(config.userName + cookies.extension)
                driver.get(config.page.get("home"))
            else:
                print("User not found, please login...")

    WebDriverWait(driver, 99999).until(  # Wait login button dissaper
        EC.invisibility_of_element_located(
            (
                By.CSS_SELECTOR,
                "body > div.page-anonymous > div > div > div.card.card-md > div > form > div > div > div.form-footer > button",
            )
        )
    )

    utils.detectErrorInLogin()

    element = WebDriverWait(driver, 99999).until(  # Expand user menu to copy name
        EC.element_to_be_clickable(
            (
                By.CSS_SELECTOR,
                "body > div.page > header > div > div.ms-md-4.d-none.d-lg-block > div > div.navbar-nav.flex-row.order-md-last.user-menu > div > a",
            )
        )
    )
    element.click()
    nameUser = (
        WebDriverWait(driver, 99999)
        .until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "body > div.page > header > div > div.ms-md-4.d-none.d-lg-block > div > div.navbar-nav.flex-row.order-md-last.user-menu > div > div > h6",
                )
            )
        )
        .get_property("innerHTML")
    )
    config.userName = nameUser.split()[0]
    print(f"Username: {config.userName}")
    cookies.saveCookie(config.userName)
    if config.saveLoginTxt == 1:
        logintxt.saveUserPass(config.userName)


def loadPresetUserInfo():
    time.sleep(config.sleeptime)

    if config.config.has_section(config.userName):
        config.sala = config.config.get(config.userName, "sala")
        config.telefone = int(config.config.get(config.userName, "telefone"))

    if config.sala == 0:
        salas_list = [1, 5, 6, 12, 13, 14, 15, 16, 17, 18, 19]
        config.sala = random.choice(salas_list)
        ramal_list = [9850, 9851, 9852, 9853, 9854]
        config.telefone = str(random.choice(ramal_list))
    else:
        salaPrefixList = ["", "Sala ", "sala "]
        config.sala = random.choice(salaPrefixList) + str(config.sala)

    if len(str(config.telefone)) == 4:
        # variables
        if random.randrange(0, 1) == 0:
            config.telefone = random.choice(["3311", "3311-", "3311 "]) + str(
                config.telefone
            )
        if random.randrange(0, 1) == 0:
            config.telefone = random.choice(["61", "61 ", "(61)", "(61) "]) + str(
                config.telefone
            )

        # match config.sala:
        # case config.sala if 0 <= config.sala <= 11:
        listAndar = [
            "terreo",
            "Térreo",
            "Terrestre",
            "Primeiro piso",
            "0",
            "Piso térreo",
            "Térreo",
            "Tér.",
            "Piso 0",
            "Andar térreo",
            "Piso um",
            "1º andar",
            "1º piso",
            "Piso principal",
            "Piso de entrada",
            "Piso de acesso",
            "Andar principal",
            "Nível 0",
            "Nível um",
            "Andar zero",
            "Nível principal",
            "Térreo superior",
            "Andar de entrada",
        ]
        config.andar = random.choice(listAndar)
        # case config.sala if 12 <= config.sala <= 20:
        #     config.andar = 1


def setPageRequest():
    time.sleep(config.sleeptime)

    if config.request_manual == 0:
        driver.get(config.page.get("userOpenRequest"))
        # if len(config.request_link) > 0:
        # driver.get(config.request_link)
        # print("config.request_link: ", config.request_link)

    # utils.waitPageLoadElementAppears()
    # time.sleep(config.sleeptime)


def setRequestInfo():

    # Category
    WebDriverWait(driver, 99999).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//*[contains(@id, 'select2-dropdown_itilcategories_id')]")
        )
    ).click()

    # WebDriverWait(driver, 99999).until(  # Wait search
    #     EC.invisibility_of_element_located(
    #         (By.XPATH, f"//*[contains(text()='Searching...')]")
    #     )
    # )

    element = WebDriverWait(driver, 99999).until(  # Closest input
        EC.element_to_be_clickable(
            (
                By.CSS_SELECTOR,
                "body > span > span > span.select2-search.select2-search--dropdown > input",
            )
        )
    )
    element.send_keys(config.request_category)
    time.sleep(1)
    element.send_keys(Keys.ENTER)

    WebDriverWait(driver, 99999).until(  # Wait list dissaper
        EC.invisibility_of_element_located(
            (By.CSS_SELECTOR, f"body > span > span > span.select2-results")
        )
    )

    # City
    WebDriverWait(driver, 99999).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//*[contains(@id, 'select2-dropdown_locations_id')]")
        )
    ).click()

    #     WebDriverWait(driver, 99999).until(  # Wait search
    #         EC.invisibility_of_element_located(
    #             (By.XPATH, f"//*[contains(text()='Searching...')]")
    #         )
    #     )

    #     Message: invalid selector
    # from javascript error: {"status":32,"value":"Unable to locate an element with the xpath expression //*[contains(text()='Searching...')] because of the following error:\nSyntaxError: Failed to execute 'evaluate' on 'Document': The string '//*[contains(text()='Searching...')]' is not a valid XPath expression."}
    #   (Session info: chrome=131.0.6778.205)

    element = WebDriverWait(driver, 99999).until(  # Closest input
        EC.element_to_be_clickable(
            (
                By.CSS_SELECTOR,
                "body > span > span > span.select2-search.select2-search--dropdown > input",
            )
        )
    )
    element.send_keys(config.city)
    time.sleep(1)
    element.send_keys(Keys.ENTER)

    WebDriverWait(driver, 99999).until(  # Wait list dissaper
        EC.invisibility_of_element_located(
            (By.CSS_SELECTOR, f"body > span > span > span.select2-results")
        )
    )

    element = WebDriverWait(driver, 99999).until(  # Closest "name_" is title
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//*[contains(@id, 'name_')]",
            )
        )
    )
    element.click()
    element.send_keys(config.request_title)

    # Text box iframe
    iframe = driver.find_element(
        By.XPATH,
        "//iframe[@title='Área de texto rico']",
    )
    driver.switch_to.frame(iframe)

    element = driver.find_element(
        By.CSS_SELECTOR,
        "#tinymce",
    )
    element.clear()

    element.send_keys("1) Unidade : ")
    element.send_keys(config.city)
    element.send_keys(Keys.ENTER)
    element.send_keys("2) Localidade (Nº da Sala / Setor / Home Office) : ")
    element.send_keys(config.sala)
    element.send_keys(Keys.ENTER)
    element.send_keys("3) Andar : ")
    element.send_keys(config.andar)
    element.send_keys(Keys.ENTER)
    element.send_keys("4) Telefone (Pessoal / Corporativo / Ramal) : ")
    element.send_keys(config.telefone)
    element.send_keys(Keys.ENTER)
    element.send_keys("5) Patrimônio (Etiqueta branca) : ")
    element.send_keys(config.request_patrimonio)
    element.send_keys(Keys.ENTER)
    element.send_keys("6) Descrição : ")
    element.send_keys(config.request_problem)
    element.send_keys(Keys.ENTER)

    driver.switch_to.default_content()

    if config.request_manual == 0:
        if config.waitConfirmOpen == 0:
            WebDriverWait(driver, 99999).until(  # button send ticket (in user form)
                EC.presence_of_element_located(
                    (
                        By.NAME,
                        f"add",
                    )
                )
            ).click()

    time.sleep(99999)

    # utils.waitPageBlockElement()

    # IF FRAME
    # # WebDriverWait(driver, 99999).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//*[@id="questionario"]')))
    driver.switch_to.frame("questionario")
    field = driver.find_elements(
        By.XPATH, '//*[@id="campoDyn_152"]'
    )  # //*[@id="campoDyn_63"]
    if field:
        field[0].click(), field[0].send_keys(config.city + Keys.ENTER)
    field = driver.find_elements(By.XPATH, '//*[@id="campoDyn_65"]')
    if field:
        field[0].click(), field[0].send_keys(config.sala)
    field = driver.find_elements(By.XPATH, '//*[@id="campoDyn_66"]')
    if field:
        field[0].click(), field[0].send_keys(config.andar)
    field = driver.find_elements(By.XPATH, '//*[@id="campoDyn_67"]')
    if field:
        field[0].click(), field[0].send_keys(config.request_patrimonio)
    field = driver.find_elements(By.XPATH, '//*[@id="campoDyn_68"]')
    if field:
        field[0].click(), field[0].send_keys(config.request_problem)
    driver.switch_to.default_content()

    # IF NOT FRAME
    element = driver.find_elements(
        By.XPATH,
        '//*[@id="tb_localidade.nome_localidade"]/div/select',
    )
    if element:
        element[0].send_keys(config.city)

    element = driver.find_elements(
        By.XPATH,
        '//*[@id="tb_localidade.Sala"]',
    )
    if element:
        ActionChains(driver).move_to_element(element[0]).click(element[0]).send_keys(
            config.sala
        ).perform()

    element = driver.find_elements(
        By.XPATH,
        '//*[@id="tb_localidade.Andar"]',
    )
    if element:
        ActionChains(driver).move_to_element(element[0]).click(element[0]).send_keys(
            config.andar
        ).perform()

    element = driver.find_elements(
        By.XPATH,
        '//*[@id="tb_localidade.Telefone"]',
    )
    if element:
        ActionChains(driver).move_to_element(element[0]).click(element[0]).send_keys(
            config.telefone
        ).perform()

    element = driver.find_elements(
        By.XPATH,
        '//*[@id="tb_localidade.Patrimonio"]',
    )
    if element:
        ActionChains(driver).move_to_element(element[0]).click(element[0]).send_keys(
            config.request_patrimonio
        ).perform()

    element = driver.find_elements(By.XPATH, '//*[@id="solicitacaoObservacao"]')
    if element:
        ActionChains(driver).move_to_element(element[0]).click(element[0]).send_keys(
            config.request_problem
        ).perform()

    print("0")
    if config.request_manual == 0:
        print("1")
        if config.waitConfirmOpen == 0:
            print("2")
            # confirm
            field = WebDriverWait(driver, 99999).until(
                EC.element_to_be_clickable((By.ID, "btn-add-servico-and-finish"))
            )

            print("3")
            field.click()

    # get request number
    try:
        element = WebDriverWait(driver, 99999).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "panel-body"))
        )
        print("painel com informações da abertura detectado")

        element = WebDriverWait(driver, 99999).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "#solicitacoes-criadas-content > div > div > div > div > div > div:nth-child(1) > h2",
                )
            )
        )
        print("numero de chamado detectado")

        element.get_attribute("outerText")
        print(element.get_attribute("outerText"))
        config.request_number = element.get_attribute("outerText")
        print("Chamado nº" + config.request_number + " aberto")
    except Exception as e:
        print("Chamado não aberto")
        print(f"Erro: {e}")
        exit()

    # time.sleep(99999)


def userLogout():
    driver.get(config.page.get("logout"))  # user logout
    time.sleep(config.sleeptime)
    driver.delete_all_cookies()
    time.sleep(config.sleeptime)
