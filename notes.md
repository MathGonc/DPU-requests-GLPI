# dpu requests

## To do:

aguardar elemento class="loading-neuro" desaparecer

Abrir e-mail e procurar e-mail de elogio

https://suporte.dpu.def.br/citsmart/pages/smartPortal/smartPortal.load#/my-requests

/html/body/div[5]/div[4]/div/div/div[5]/form/div[2]/div/div[2]/select
//\*[@id="idStatusMinhasSolicitacoes"]

Todos

/html/body/div[5]/div[4]/div/div/div[5]/form/div[2]/div/div[5]/button/i
//\*[@id="formMinhasSolicitacoes"]/div[2]/div/div[5]/button/i

Opnião:
/html/body/div[5]/div[4]/div/div/div[5]/form/div[4]/div[1]/div/div[2]/button[2]/i
//\*[@id="actions-24966"]/button[3]

Esperar sumir:

<div class="loading-neuro"><span>undefined</span></div>

# Tricks:

target_text = "Nenhum registro encontrado!"
elements_with_text = config.driver.find_elements(By.XPATH, "//\*[contains(text(), '{}')]".format(target_text))

    # Verificar se a lista de elementos não está vazia, indicando que o texto foi encontrado
    if elements_with_text:
        print(f"O texto '{target_text}' foi encontrado na página.")
    else:
        print(f"O texto '{target_text}' não foi encontrado na página.")

## -

from selenium.common.exceptions import NoSuchElementException

def find_element_safely(driver, selector):
try:
element = driver.find_element(\*selector)
return element
except NoSuchElementException:
return None
