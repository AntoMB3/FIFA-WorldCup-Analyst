import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

## Leer el driver de Chrome para poder utilizarlo
path = "D:\Proyectos\chromedriver_win32\chromedriver.exe"
service = Service(executable_path=path)


#Activar el driver
driver = webdriver.Chrome(service=service)

driver.get("https://es.wikipedia.org/wiki/Copa_Mundial_de_F%C3%BAtbol_de_2018")
time.sleep(15)
driver.quit()