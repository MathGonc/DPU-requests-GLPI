from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import config
import menu
import utils
import cookies
import random


def rateRequest():
    login()
    setUserInfo()
    config.driver.get(config.page.get("rate"))

    element = WebDriverWait(config.driver, 9999).until(
        EC.presence_of_element_located((By.ID, "idStatusMinhasSolicitacoes"))
    )
    time.sleep(config.sleeptime)
    element.click()
    element.send_keys("Todos" + Keys.ENTER)
    time.sleep(config.sleeptime)

    button = config.driver.find_element(
        By.CSS_SELECTOR,
        f"#formMinhasSolicitacoes > div.row > div > div.col-md-1 > button",
    )
    time.sleep(config.sleeptime)
    button.click()
    time.sleep(config.sleeptime)

    element = config.driver.find_elements(By.XPATH, f"//i[text()='thumbs_up_down']")
    utils.alert(f"{len(element)} chamados a serem avaliados")

    time.sleep(9999)


def OpenRequest():
    login()
    setUserInfo()
    setPageRequest()
    setRequestInfo()
    userLogout()


def login():
    config.driver.get(config.page.get("login"))

    if len(config.userLoginName) == 0:
        WebDriverWait(config.driver, 9999).until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/nav/div/div[1]/a/img")
            )
        )  # logo dpu

        nameUser = config.driver.find_element(
            By.XPATH, '// *[ @ id = "navbar"] / ul / li[4] / a / span[1]'
        ).text
        cookies.saveCookie(nameUser.split()[0])


def setUserInfo():
    time.sleep(config.sleeptime)
    cookies.loadCookie(config.userLoginName + cookies.extension)

    if config.config.has_section(config.userLoginName):
        config.sala = int(config.config.get(config.userLoginName, "sala"))
        config.telefone = int(config.config.get(config.userLoginName, "telefone"))

    if config.sala == 0:
        salas_list = [1, 5, 6, 12, 13, 14, 15, 16, 17, 18, 19]
        config.sala = random.choice(salas_list)
        ramal_list = [9850, 9851, 9852, 9853, 9854]
        config.telefone = str(random.choice(ramal_list))

    # random add 3311 or not
    if len(str(config.telefone)) == 4:
        match random.randint(0, 2):
            case 0:
                config.telefone = config.telefone
            case 1:
                config.telefone = "3311" + str(config.telefone)
            case 2:
                config.telefone = "3311-" + str(config.telefone)

    match config.sala:
        case config.sala if 0 <= config.sala <= 11:
            config.andar = "terreo"
        case config.sala if 12 <= config.sala <= 20:
            config.andar = 1


def setPageRequest():
    time.sleep(config.sleeptime)

    if config.request_manual == 0:
        if len(config.request_link) > 0:
            config.driver.get(config.request_link)

    WebDriverWait(config.driver, 9999).until(
        EC.presence_of_element_located((By.ID, "btn-add-servico-and-finish"))
    )
    time.sleep(config.sleeptime)


def setRequestInfo():
    # IF FRAME
    # WebDriverWait(config.driver, 9999).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//*[@id="questionario"]')))
    config.driver.switch_to.frame("questionario")
    field = config.driver.find_elements(
        By.XPATH, '//*[@id="campoDyn_152"]'
    )  # //*[@id="campoDyn_63"]
    if field:
        field[0].click(), field[0].send_keys(config.city + Keys.ENTER)
    field = config.driver.find_elements(By.XPATH, '//*[@id="campoDyn_65"]')
    if field:
        field[0].click(), field[0].send_keys(config.sala)
    field = config.driver.find_elements(By.XPATH, '//*[@id="campoDyn_66"]')
    if field:
        field[0].click(), field[0].send_keys(config.andar)
    field = config.driver.find_elements(By.XPATH, '//*[@id="campoDyn_67"]')
    if field:
        field[0].click(), field[0].send_keys(config.request_patrimonio)
    field = config.driver.find_elements(By.XPATH, '//*[@id="campoDyn_68"]')
    if field:
        field[0].click(), field[0].send_keys(config.request_problem)
    config.driver.switch_to.default_content()

    # IF NOT FRAME
    field = config.driver.find_elements(
        By.XPATH,
        "/html/body/div[5]/div[4]/div/div/div[1]/div/div/div[3]/div/div[3]/div[1]/div/div/div/form/div[1]/div[1]/div/div/select",
    )
    if field:
        field[0].send_keys(config.city)

    field = config.driver.find_elements(
        By.XPATH,
        "/html/body/div[5]/div[4]/div/div/div[1]/div/div/div[3]/div/div[3]/div[1]/div/div/div/form/div[1]/div[2]/div/div/input",
    )
    if field:
        field[0].send_keys(config.sala)

    field = config.driver.find_elements(
        By.XPATH,
        "/html/body/div[5]/div[4]/div/div/div[1]/div/div/div[3]/div/div[3]/div[1]/div/div/div/form/div[1]/div[3]/div/div/input",
    )
    if field:
        field[0].send_keys(config.andar)

    field = config.driver.find_elements(
        By.XPATH,
        "/html/body/div[5]/div[4]/div/div/div[1]/div/div/div[3]/div/div[3]/div[1]/div/div/div/form/div[2]/div[1]/div/input",
    )
    if field:
        field[0].send_keys(config.telefone)

    field = config.driver.find_elements(
        By.XPATH,
        "/html/body/div[5]/div[4]/div/div/div[1]/div/div/div[3]/div/div[3]/div[1]/div/div/div/form/div[2]/div[2]/div/div/input",
    )
    if field:
        field[0].send_keys(config.request_patrimonio)

    field = config.driver.find_elements(By.XPATH, '//*[@id="solicitacaoObservacao"]')
    if field:
        field[0].send_keys(config.request_problem)

    if config.request_manual == 0:
        # confirm
        field = config.driver.find_elements(
            By.XPATH, '//*[@id="btn-add-servico-and-finish"]'
        )
        if field:
            field[0].click()
        time.sleep(15)

    # get request number
    try:
        WebDriverWait(config.driver, 1000).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "/html/body/div[6]/div/div/div[2]/div/div/div/div/div/div[1]/h2",
                )
            )
        )
        getRequestNumber = config.driver.find_element(
            By.XPATH, "/html/body/div[6]/div/div/div[2]/div/div/div/div/div/div[1]/h2"
        ).get_attribute("outerText")
        config.request_number = getRequestNumber
        print("Chamado nº" + getRequestNumber + " aberto")
    except:
        print("Chamado não aberto")
        exit()

    time.sleep(config.sleeptime)


def userLogout():
    config.driver.get(config.page.get("logout"))  # user logout
    time.sleep(config.sleeptime)
    config.driver.delete_all_cookies()
