from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert

import time
import config
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


def waitPageBlockElement():
    WebDriverWait(driver, 99999).until(
        EC.invisibility_of_element_located((By.CLASS_NAME, "loading-neuro"))
    )

    WebDriverWait(driver, 99999).until(
        EC.invisibility_of_element_located(
            (By.ID, "divBloqueiaTela_JANELA_AGUARDE_MENU")
        )
    )


def verifyPageErrorExist():
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"//span[text()='undefined']"))
        )
        print("Error undefined in loading-neuro, reloading...")
        driver.refresh()
        return True
    except:
        print("loading-neuro show with success")
        return False


def verifyBrowserIsOpen():
    try:
        driver.find_element(By.TAG_NAME, "body")
        return True
    except:
        return False
