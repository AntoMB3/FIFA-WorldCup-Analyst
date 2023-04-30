import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

## Leer el driver de Chrome para poder utilizarlo
path = "D:\Proyectos\chromedriver_win32\chromedriver.exe"
service = Service(executable_path=path)


#Activar el driver
driver = webdriver.Chrome(service=service)

mundiales = [1930,1934,1938]
mundiales = mundiales + [i for i in range(1950,2019,4)]

def GetMundial(year):
    driver.get(f"https://es.wikipedia.org/wiki/Copa_Mundial_de_F%C3%BAtbol_de_{year}")
    #driver.get(f"https://en.wikipedia.org/wiki/{year}_FIFA_World_Cup")

    partidos = driver.find_elements(by="xpath",value='//table [@class = "collapsible autocollapse vevent plainlist"]')

    local = []
    visitante = []
    marcador = []
    for partido in partidos:
        local.append(partido.find_element(by="xpath",value='.//td[@width = "24%"]').text)
        visitante.append(partido.find_element(by="xpath",value='.//td[@width = "22%"]').text)
        marcador.append(partido.find_element(by="xpath",value='.//td[@width = "12%"]').text)

    dict_partidos = {"Local": local, "Visitante": visitante, "Marcador":marcador}
    df_partidos = pd.DataFrame(dict_partidos)
    df_partidos["Año"] = year
    return df_partidos

lista_mundiales = [GetMundial(mundial) for mundial in mundiales]
Fifa_worldcup = pd.concat(lista_mundiales, ignore_index=True)
Fifa_worldcup.to_csv("data/mundiales.csv",index=False)
driver.quit()