# dpu requests

## To do:

Incluir adm automaticamente nos chamados
Excluir também chamados observados para não contar

# Tricks:

target_text = "Nenhum registro encontrado!"
elements_with_text = driver.find_elements(By.XPATH, "//\*[contains(text(), '{}')]".format(target_text))

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
