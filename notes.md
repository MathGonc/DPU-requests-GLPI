# dpu requests

## To do:

Caso não encontre nenhum documento na base de conhecimento, não continuar no modo automatico
aguardar elemento class="loading-neuro" desaparecer.

---

Resolver o erro:
alert.accept()

Exception has occurred: NoAlertPresentException
Message: no such alert
(Session info: chrome=127.0.6533.89)
Stacktrace:
GetHandleVerifier [0x00007FF6EE7AEEA2+31554]
(No symbol) [0x00007FF6EE727ED9]
(No symbol) [0x00007FF6EE5E8559]
(No symbol) [0x00007FF6EE5D850A]
(No symbol) [0x00007FF6EE60C3CA]
(No symbol) [0x00007FF6EE65D0DD]
(No symbol) [0x00007FF6EE60BBFB]
(No symbol) [0x00007FF6EE65CDD3]
(No symbol) [0x00007FF6EE62A33B]
(No symbol) [0x00007FF6EE62AED1]
GetHandleVerifier [0x00007FF6EEAB8B1D+3217341]
GetHandleVerifier [0x00007FF6EEB05AE3+3532675]
GetHandleVerifier [0x00007FF6EEAFB0E0+3489152]
GetHandleVerifier [0x00007FF6EE85E776+750614]
(No symbol) [0x00007FF6EE73375F]
(No symbol) [0x00007FF6EE72EB14]
(No symbol) [0x00007FF6EE72ECA2]
(No symbol) [0x00007FF6EE71E16F]
BaseThreadInitThunk [0x00007FFF39287034+20]
RtlUserThreadStart [0x00007FFF3AA02651+33]

---

Resolver o erro:
Message: element click intercepted: Element <button id="request-save-submit" type="button" ng-click="processSaveOrUpdate(salvarAvancar)" ng-show="permission.habilitaGravarEContinuar == 'S'" class="btn btn-citsmart btn-sm" ng-disabled="disableSaveActionButton" style="">...</button> is not clickable at point (1820, 932). Other element would receive the click: <div modal-render="true" tabindex="-1" role="dialog" class="modal fade ng-isolate-scope in" uib-modal-animation-class="fade" modal-in-class="in" ng-style="{'z-index': 1050 + index*10, display: 'block'}" uib-modal-window="modal-window" window-class="" size="lg" index="1" animate="animate" modal-animation="true" style="z-index: 1060; display: block;">...</div>

---

Abrir e-mail e procurar e-mail de elogio

---

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
