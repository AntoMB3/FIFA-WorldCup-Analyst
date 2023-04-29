import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
import re
from string import ascii_uppercase as alfabeto
import pickle

## Leer el driver de Chrome para poder utilizarlo
path = "D:\Proyectos\chromedriver_win32\chromedriver.exe"
service = Service(executable_path=path)

#Activar el driver
driver = webdriver.Chrome(service=service)

driver.get("https://web.archive.org/web/20221115040351/https://en.wikipedia.org/wiki/2022_FIFA_World_Cup")

dict_grupos = {}

for letra, grupo in zip(alfabeto,range(7,15,1)):

    partido = driver.find_element(by="xpath",value=f'//*[@id="mw-content-text"]/div[1]/table[{grupo}]')

    ######## Limpieza de datos
    tabla = partido.text.split(" ")

    tabla_clean = []
    for elemento in tabla:
        if(elemento != ''):
            tabla_clean.append(elemento)


    i = 0
    for elemento in tabla_clean:
        tabla_clean[i] = re.sub(r'\n\d+',"",elemento)
        i += 1


    columnas = tabla_clean[:10]
    del tabla_clean[:10]

    columnas[1] = columnas[1][:4]
    del columnas[-1]
    del columnas[0]

    bad_words = ['Advance', 'to', 'knockout', 'stage']

    for word in bad_words:
        while word in tabla_clean:
            tabla_clean.remove(word)

    if('Qatar' in tabla_clean):
        index_qatar = tabla_clean.index('Qatar')
        concatenado = tabla_clean[index_qatar]+tabla_clean[index_qatar+1]
        tabla_clean[index_qatar] = concatenado
        del tabla_clean[index_qatar+1]
    ################################################





    dict_tabla = {'Pos':[i+1 for i in range(4)],'Team':[],'W':[],'D':[],'L':[],'GF':[],'GA':[],'GD':[],'Pts':[]}

    i = 0
    for team in range(4):
        for stat in columnas:
            if(tabla_clean[i+1] != '0' and stat == "Team"):
                tabla_clean[i+1] = tabla_clean[i]+" "+tabla_clean[i+1]
                i += 1

            dict_tabla[stat].append(tabla_clean[i])
            i+=1
        i+=1


    df_Tabla = pd.DataFrame(dict_tabla)

    dict_grupos[f"Grupo {letra}"] = df_Tabla

with open("data/dict_grupos.pkl","wb") as archivo:
    pickle.dump(dict_grupos,archivo)

archivo.close()

for tablas in  dict_grupos.keys():
    print(dict_grupos[tablas])

driver.quit()


