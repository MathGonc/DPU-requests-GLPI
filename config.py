from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")

driver = ""
page = {
    "home": "https://suporte.dpu.def.br/",
    "login": "https://suporte.dpu.def.br/",
    "logout": "https://suporte.dpu.def.br/citsmart/logout",
    "admin": "https://suporte.dpu.def.br/citsmart/pages/serviceRequestIncident/serviceRequestIncident.load#/",
    "userOpenRequest": "https://suporte.dpu.def.br/citsmart/pages/smartPortal/smartPortal.load",
    "admin_requestid": "https://suporte.dpu.def.br/citsmart/pages/serviceRequestIncident/serviceRequestIncident.load#/request?idRequest=",
    "rate": "https://suporte.dpu.def.br/citsmart/pages/smartPortal/smartPortal.load#/my-requests",
}

sleeptime = 3
looptime = 300

# geral
needMedia = config.get("default", "needMedia")
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
