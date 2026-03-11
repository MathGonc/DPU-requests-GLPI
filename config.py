from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini", encoding="utf-8")

page = {
    "home": "https://suporte.dpu.def.br/",
    "login": "https://suporte.dpu.def.br/",
    "logout": "https://suporte.dpu.def.br/front/logout.php?noAUTO=1",
    "adminRequestList": "https://suporte.dpu.def.br/front/ticket.php?is_deleted=0&as_map=0&browse=0&criteria%5B0%5D%5Blink%5D=AND&criteria%5B0%5D%5Bfield%5D=12&criteria%5B0%5D%5Bsearchtype%5D=equals&criteria%5B0%5D%5Bvalue%5D=notold&criteria%5B1%5D%5Blink%5D=AND&criteria%5B1%5D%5Bfield%5D=83&criteria%5B1%5D%5Bsearchtype%5D=contains&criteria%5B1%5D%5Bvalue%5D=CAMPO%20GRANDE&itemtype=Ticket&start=0&_glpi_csrf_token=e19ded95b3a3867f37c312fefb39a8b8b49e0a538d41b8c062310908595feeb2&sort%5B%5D=19&order%5B%5D=DESC",
    "createRequestUserPanel": "https://suporte.dpu.def.br/front/helpdesk.public.php?create_ticket=1",
    "createRequestAdminPanel": "https://suporte.dpu.def.br/front/ticket.form.php",
    "admin_requestid": "https://suporte.dpu.def.br/front/ticket.form.php?id=",
    "rate": "https://suporte.dpu.def.br/citsmart/pages/smartPortal/smartPortal.load#/my-requests",
}

sleeptime = 0
looptime = 60

# geral
needMedia = int(config.get("default", "needMedia"))
waitConfirmOpen = int(config.get("default", "waitConfirmOpen"))
waitConfirmClose = int(config.get("default", "waitConfirmClose"))
defaultOption = int(config.get("default", "defaultOption"))
defaultUser = int(config.get("default", "defaultUser"))
defaultRequest = int(config.get("default", "defaultRequest"))
defaultPatrimonio = int(config.get("default", "defaultPatrimonio"))
saveLoginTxt = int(config.get("default", "saveLoginTxt"))
city = config.get("default", "city")
adminUser = config.get("default", "adminUser")

# user
userLoginName = ""
userLoginPass = ""
userName = ""
sala = 0
andar = ""
telefone = ""

# request
request_number = "0"
request_path = r"./requests"
request_manual = 0

# request file
request_title = ""
request_patrimonio = ""
request_link = ""
request_problem = ""
request_category = ""
request_class_solution = ""
request_solution = ""
request_knowledge = ""
