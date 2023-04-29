import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

## Leer el driver de Chrome para poder utilizarlo
path = "D:\Proyectos\chromedriver_win32\chromedriver.exe"
service = Service(executable_path=path)

#Activar el driver
driver = webdriver.Chrome(service=service)

driver.get("https://web.archive.org/web/20221115040351/https://en.wikipedia.org/wiki/2022_FIFA_World_Cup")

partidos = driver.find_elements(by="xpath",value='//tr[@itemprop = "name"]')

local = []
visitante = []
marcador = []
for partido in partidos:
    local.append(partido.find_element(by="xpath",value='.//th[@class = "fhome"]').text)
    visitante.append(partido.find_element(by="xpath",value='.//th[@class = "faway"]').text)
    marcador.append(partido.find_element(by="xpath",value='.//th[@class = "fscore"]').text)

dict_partidos = {"Local": local, "Visitante": visitante, "Marcador":marcador}
df_partidos = pd.DataFrame(dict_partidos)
df_partidos["Año"] = 2022

df_partidos.to_csv("data/partidosQatar.csv",index=False)

driver.quit()