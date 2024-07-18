from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini", encoding="utf-8")

page = {
    "home": "https://suporte.dpu.def.br/",
    "login": "https://suporte.dpu.def.br/",
    "logout": "https://suporte.dpu.def.br/citsmart/logout",
    "admin": "https://suporte.dpu.def.br/citsmart/pages/serviceRequestIncident/serviceRequestIncident.load#/",
    "userOpenRequest": "https://suporte.dpu.def.br/citsmart/pages/smartPortal/smartPortal.load",
    "admin_requestid": "https://suporte.dpu.def.br/citsmart/pages/serviceRequestIncident/serviceRequestIncident.load#/request?idRequest=",
    "rate": "https://suporte.dpu.def.br/citsmart/pages/smartPortal/smartPortal.load#/my-requests",
}

sleeptime = 1
looptime = 300

# geral
needMedia = int(config.get("default", "needMedia"))
waitConfirmOpen = int(config.get("default", "waitConfirmOpen"))
waitConfirmClose = int(config.get("default", "waitConfirmClose"))
defaultOption = int(config.get("default", "defaultOption"))
defaultUser = int(config.get("default", "defaultUser"))
defaultRequest = int(config.get("default", "defaultRequest"))
defaultPatrimonio = int(config.get("default", "defaultPatrimonio"))
city = config.get("default", "city")

# user
userLoginName = ""
userLoginPass = ""
sala = 0
andar = ""
telefone = ""

# request
request_number = "0"
request_path = r"./requests"
request_manual = 0

# request file
request_patrimonio = ""
request_link = ""
request_problem = ""
request_class_cause = ""
request_class_solution = ""
request_solution = ""
request_knowledge = ""
