from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re  # To extract number request

import time
import config
import utils
import cookies
import random
import logintxt
import driver as drv

driver = drv.get_driver()


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
            driver.get(config.page["adminRequestList"])
        elif len(config.userName) > 0:
            logintxt.loadUserPass(config.userName)
            logintxt.inputLogin()
            driver.get(config.page.get("home"))
        else:
            logintxt.inputUserPass()
    else:  # Load via cookies
        if admin == 1:
            cookies.loadCookie(cookies.cookieAdminFile)
            driver.get(config.page["adminRequestList"])
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
        if admin == 1:
            logintxt.saveUserPass("ADMIN")


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


def setPageRequest(form=0):
    time.sleep(config.sleeptime)

    if config.request_manual == 0:

        if form == 0:
            driver.get(config.page.get("createRequestUserPanel"))
        else:
            print("config.request_link: ", config.request_link)
            if not len(config.request_link):
                driver.get(config.page.get("createRequestUserPanel"))
            else:
                driver.get(config.request_link)

    # utils.waitPageLoadElementAppears()
    # time.sleep(config.sleeptime)


def setRequestInfo(form=0):

    # In this moment, only tec=0 is called
    # There are 2 call forms, 1 for technicians and 1 for users

    if form == 0:
        # ----- Category
        WebDriverWait(driver, 99999).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[contains(@id, 'select2-dropdown_itilcategories_id')]")
            )
        ).click()

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

        # -----

        # ----- City -----
        WebDriverWait(driver, 99999).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[contains(@id, 'select2-dropdown_locations_id')]")
            )
        ).click()

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

        # ----------

        # ----- Title
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

        # -----

        # ----- Text box iframe -----
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
        # ----------

    else:  # User ticket form

        # ----- City -----
        element = WebDriverWait(driver, 99999).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//div[contains(@data-itemtype, 'PluginFormcreatorQuestion')][.//label[contains(text(), 'Unidade')]]//span[text()='-----']",
                )
            )
        )
        ActionChains(driver).move_to_element(element).perform()
        element.click()

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

        # ----------

        # ----- OPTIONAL: Programas -----
        element = driver.find_elements(
            By.XPATH,
            "//div[contains(@data-itemtype, 'PluginFormcreatorQuestion')][.//label[contains(text(), 'Tipo de atendimento')]]//span[text()='-----']",
        )
        if element:
            element[0].click()
            time.sleep(1)

            key_down = random.randint(0, 2)
            print("key_down: ", key_down)
            for i in range(key_down):
                ActionChains(driver).send_keys(Keys.ARROW_DOWN).perform()
            ActionChains(driver).send_keys(Keys.ENTER).perform()

        element = driver.find_elements(
            By.XPATH,
            "//div[contains(@data-itemtype, 'PluginFormcreatorQuestion')][.//label[contains(text(), 'Programa')]]//span[text()='-----']",
        )
        if element:
            element[0].click()
            time.sleep(1)

            key_down = random.randint(0, 13)
            print("key_down: ", key_down)
            for i in range(key_down):
                ActionChains(driver).send_keys(Keys.ARROW_DOWN).perform()
                print(f"Key_down: {i}")
            ActionChains(driver).send_keys(Keys.ENTER).perform()

        # OPTIONAL: Create user
        element = driver.find_elements(
            By.XPATH,
            "//div[contains(@class, 'grid-stack-item-content')][.//label[contains(text(), 'E-mail')]]//input[@type='text']",
        )
        if element:
            element[0].send_keys("rh.ms@dpu.def.br")
            time.sleep(1)

        element = driver.find_elements(
            By.XPATH,
            "//div[contains(@class, 'grid-stack-item-content')][.//label[contains(text(), 'O novo usuário é um estagiário?')]]//span[text()='-----']",
        )
        if element:
            element[0].click()
            ActionChains(driver).send_keys(Keys.ARROW_DOWN).perform()
            ActionChains(driver).send_keys(Keys.ENTER).perform()
            time.sleep(1)

        element = driver.find_elements(
            By.XPATH,
            "//div[contains(@class, 'grid-stack-item-content')][.//label[contains(text(), 'Será necessário acesso a pastas de rede?')]]//span[text()='-----']",
        )
        if element:
            element[0].click()
            ActionChains(driver).send_keys(Keys.ARROW_DOWN).perform()
            ActionChains(driver).send_keys(Keys.ENTER).perform()
            time.sleep(1)

        element = driver.find_elements(
            By.XPATH,
            "//div[contains(@class, 'grid-stack-item-content')][.//label[contains(text(), 'Nome e caminho da pasta')]]//input[@type='text']",
        )
        if element:
            element[0].send_keys(f"\\\CPE-ARQ-PVW02\DPUCPE")

        element = driver.find_elements(
            By.XPATH,
            "//div[contains(@class, 'grid-stack-item-content')][.//label[contains(text(), 'Será necessário a criação de e-mail institucional?')]]//span[text()='Sim']",
        )
        if element:
            element[0].click()
            ActionChains(driver).send_keys(Keys.ARROW_DOWN).perform()
            ActionChains(driver).send_keys(Keys.ENTER).perform()
            time.sleep(1)

        # ----------

        # # In Order: Local, Andar, Telefone & Patrimonio
        # element = driver.find_elements(
        #     By.XPATH,
        #     f"//input[contains(@class, 'form-control') and not(@name='globalsearch')]",  # @name='globalsearch' is for not input in search field (showed for admin)
        # )
        # print(f"input fields: {len(element)}")
        # element[0].send_keys(config.sala)
        # element[1].send_keys(config.andar)
        # element[2].send_keys(config.telefone)
        # element[3].send_keys(config.request_patrimonio)

        element = driver.find_elements(
            By.XPATH,
            "//div[contains(@class, 'grid-stack-item-content')][.//label[contains(text(), 'Localidade')]]//input[@type='text']",
        )
        if element:
            element[0].send_keys(config.sala)

        element = driver.find_elements(
            By.XPATH,
            "//div[contains(@class, 'grid-stack-item-content')][.//label[contains(text(), 'Andar')]]//input[@type='text']",
        )
        if element:
            element[0].send_keys(config.andar)

        element = driver.find_elements(
            By.XPATH,
            "//div[contains(@class, 'grid-stack-item-content')][.//label[contains(text(), 'Telefone')]]//input[@type='text']",
        )
        if element:
            element[0].send_keys(config.telefone)

        element = driver.find_elements(
            By.XPATH,
            "//div[contains(@class, 'grid-stack-item-content')][.//label[contains(text(), 'Patrimônio')]]//input[@type='text']",
        )
        if element:
            element[0].send_keys(config.request_patrimonio)

        # ----- Text box iframe -----
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

        element.send_keys(config.request_problem)
        element.send_keys(Keys.ENTER)

        driver.switch_to.default_content()
        # ----------

    if config.request_manual == 0:
        if config.waitConfirmOpen == 0:
            element = driver.find_element(
                By.XPATH, f"//span[contains(text(), 'Enviar')]"
            ).click()

    WebDriverWait(driver, 99999).until(
        EC.invisibility_of_element((By.XPATH, f"//span[contains(text(), 'Enviar')]"))
    )
    element = WebDriverWait(driver, 99999).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//div[@class='toast-body']//a[contains(@href, '/front/ticket.form.php?id=')]",
            )
        )
    )
    text = element.get_property("href")
    print(text)
    numberTicket = re.search(r"id=(\d+)", text).group(
        1
    )  # Example: Extract "479" from "?id=479&forcetab=Ticket$2"
    config.request_number = int(numberTicket)
    print(config.request_number)
    print(f"Chamado {numberTicket} aberto")
    time.sleep(5)
    userLogout()


def userLogout():
    driver.get(config.page.get("logout"))  # user logout
    time.sleep(config.sleeptime)
    driver.delete_all_cookies()
    time.sleep(config.sleeptime)
