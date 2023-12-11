from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert

import time
import config


def alert(string, delay=5):
    try:
        # Exibir o alerta usando JavaScript
        config.driver.execute_script(f"alert('{string}');")

        # Aguardar e lidar com o alerta
        alert = WebDriverWait(config.driver, 10).until(EC.alert_is_present())
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
    WebDriverWait(config.driver, 9999).until(
        EC.invisibility_of_element_located((By.CLASS_NAME, "loading-neuro"))
    )

    WebDriverWait(config.driver, 9999).until(
        EC.invisibility_of_element_located(
            (By.ID, "divBloqueiaTela_JANELA_AGUARDE_MENU")
        )
    )

    return
