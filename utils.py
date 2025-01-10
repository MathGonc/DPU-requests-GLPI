from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import TimeoutException

import time
import config
import cookies
import user
from driver import driver


def setManualMode(mode):
    config.request_manual = mode
    print("Modo manual: " + str(config.request_manual))


def alert(string, delay=5):
    try:
        # Exibir o alerta usando JavaScript
        driver.execute_script(f"alert('{string}');")

        # Aguardar e lidar com o alerta
        alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
        if alert:
            alert_text = alert.text
            print("Alert Text:", alert_text)

            # Pausa para observar o alerta na tela (por padrão, 5 segundos)
            time.sleep(delay)

            # Aceitar o alerta (clicar em OK)
            alert.accept()
            # Ou rejeitar o alerta (clicar em Cancelar)
            # alert.dismiss()
    except Exception as e:
        print("Erro:", e)


def waitPageLoadElementAppears():
    WebDriverWait(driver, 99999).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "loading-neuro"))
    )
    print("elemento de carregamento visivel")


def waitPageBlockElement():
    WebDriverWait(driver, 99999).until(
        EC.invisibility_of_element_located((By.CLASS_NAME, "loading-neuro"))
    )
    print("elemento de carregamento invisivel")

    WebDriverWait(driver, 99999).until(
        EC.invisibility_of_element_located(
            (By.ID, "divBloqueiaTela_JANELA_AGUARDE_MENU")
        )
    )


def verifyPageErrorExist():
    try:
        elements = driver.find_elements(By.XPATH, "//span[text()='undefined']")
        if elements:
            print("Error undefined in loading-neuro, reloading...")
            driver.refresh()
            return True
        else:
            print("loading-neuro show with success")
            return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False


def verifyBrowserIsOpen():
    try:
        driver.find_element(By.TAG_NAME, "body")
        return True
    except:
        return False


def detectErrorInLogin():

    try:  # Waiting for home page is loaded
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.CLASS_NAME,
                    "navbar-brand",
                )
            )
        )
        return 1

    except:  # Home page dont loaded, can be cookies error
        elementError1 = driver.find_elements(
            By.CSS_SELECTOR,
            "body > div > div > div > div.card.card-md > div > div > div",
        )

        elementError2 = driver.find_elements(
            By.XPATH, f"//*[text()='ERR_TOO_MANY_REDIRECTS']"
        )

        if elementError1:
            print("Cookies error 1, clearing cookies, please login again...")
            time.sleep(1)
            cookies.clearCookies()
            driver.refresh()
            detectErrorInLogin()
        elif elementError2:
            print("Cookies error 2, clearing cookies, please login again...")
            time.sleep(1)
            cookies.clearCookies()
            driver.refresh()
            detectErrorInLogin()
        else:
            print(
                "Cookies error 3, User home page dont loaded, clearing cookies, please login again..."
            )
            time.sleep(1)
            cookies.clearCookies()
            driver.refresh()
            detectErrorInLogin()
        return 0
