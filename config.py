from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")

driver = ""
page = {
    "login": "https://suporte.dpu.def.br/",
    "logout": "https://suporte.dpu.def.br/citsmart/logout",
    "admin": "https://suporte.dpu.def.br/citsmart/pages/serviceRequestIncident/serviceRequestIncident.load#/",
    "user_requests": "https://suporte.dpu.def.br/citsmart/pages/smartPortal/smartPortal.load#/my-requests",
    "admin_requestid": "https://suporte.dpu.def.br/citsmart/pages/serviceRequestIncident/serviceRequestIncident.load#/request?idRequest=",
}

sleeptime = 1
looptime = 300

# geral
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
