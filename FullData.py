# %%
import pandas as pd
import pickle
from scipy.stats import poisson
import math
import random

# %% [markdown]
# ### Leer Data

primer_lugar = []
segundo_lugar = []
tercer_lugar = []
cuarto_lugar = []

for _ in range(1000):
# %%
    with open("data/dict_grupos.pkl","rb") as archivo:
        dict_grupos2022 = pickle.load(archivo)
    archivo.close()

    df_FIFA_Historical = pd.read_csv("data/FIFAWC.csv")
    df_Qatar = pd.read_csv("data/clean_Qatar.csv")



    # %%
    ## Extraer data de local y visitante por separado
    df_Local = df_FIFA_Historical[["Local","GolesLocal","GolesVisita"]].copy()
    df_visita = df_FIFA_Historical[["Visitante","GolesLocal","GolesVisita"]].copy()
    df_Local

    # %%
    ##3 Renombrar columnas
    df_Local.rename(columns={"Local":"Equipo", "GolesLocal":"GolesAnotados","GolesVisita":"GolesRecibidos"},inplace=True)
    df_visita.rename(columns={"Visitante":"Equipo", "GolesLocal":"GolesRecibidos","GolesVisita":"GolesAnotados"},inplace=True)
    df_visita

    # %%
    ## Concatenamos en un dataframe
    equipos = pd.concat([df_Local,df_visita],ignore_index=True)

    ### Agrupamos por equipo y obtenemos el promedio de cada columna
    fuerza_equipos = equipos.groupby(["Equipo"]).mean()
    fuerza_equipos

    # %%
    fuerza_equipos.loc["Irán",]
    fuerza_equipos.loc["Estados Unidos",]

    # %%
    fuerza_equipos.index

    # %%
    def Poisson(x,l):
        return (l**x * math.e**(-l))/math.factorial(x)

    def WinnerFirstWC():
        x = random.randint(0,100)
        if x <= 80:
            return (0,3)
        elif x > 80 and x < 95:
            return(1,1)
        else:
            return (3,0)

    # %%
    def Predecir_Puntos(local, visita):
        if local in fuerza_equipos.index and visita in fuerza_equipos.index:
            lambda_local = fuerza_equipos.loc[local,"GolesAnotados"]*fuerza_equipos.loc[visita,"GolesRecibidos"]
            lambda_visita = fuerza_equipos.loc[visita,"GolesAnotados"]*fuerza_equipos.loc[local,"GolesRecibidos"]

            local = 0
            visita = 0
            empate = 0
            for x in range(9):
                for y in range(9):
                    p_local = Poisson(x=x,l=lambda_local)
                    p_visita = Poisson(x=y, l = lambda_visita)
                    prob = p_local*p_visita

                    if x == y:
                        empate += prob
                    elif x > y:
                        local += prob
                    else:
                        visita += prob

            puntos_local = 3*local + empate
            puntos_visita = 3*visita + empate
            #return (round(puntos_local,0), round(puntos_visita,0))
            return (puntos_local,puntos_visita)

        else:
            if local not in fuerza_equipos.index:
                return(WinnerFirstWC())
            else:
                tupla = WinnerFirstWC()
                return tupla[::-1]


    # %%
    grupos = df_Qatar[:48].copy()
    octavos = df_Qatar[48:56].copy()
    cuartos = df_Qatar[56:60].copy()
    semis = df_Qatar[60:62].copy()
    tercer = df_Qatar[62:63].copy()
    final = df_Qatar[63:64].copy()


# %%

#Obtener partidos por grupo
    for grupo in dict_grupos2022.keys():
        equipos_en_grupo = dict_grupos2022[grupo]["Selección"].values
        partidos_grupo = grupos[grupos["Local"].isin(equipos_en_grupo)]

        tabla = dict_grupos2022[grupo]

        #Actualizar la tabla
        for partido,row in partidos_grupo.iterrows():
            local = row["Local"]
            visitante = row["Visitante"]
            puntosLocal, puntosVisitante = Predecir_Puntos(local=local,visita=visitante)

            tabla.loc[tabla["Selección"] == local, "Pts"] += puntosLocal
            tabla.loc[tabla["Selección"] == visitante, "Pts"] += puntosLocal
            tabla.sort_values("Pts",axis=0,ascending = False,inplace=True)
        
        tabla["Pos"] = [i+1 for i in range(4)]

    


    # %%


    # %%
    octavos

    # %%
    ### Obtener partidos de octavos

    locales = octavos["Local"].str.split(".° ")
    for local,equipo in zip(octavos["Local"],locales):
        equipo_local = str(dict_grupos2022[equipo[1]].loc[dict_grupos2022[equipo[1]]["Pos"] == int(equipo[0]), "Selección"].values[0])
        octavos.replace(local,equipo_local,inplace=True)

    locales = octavos["Visitante"].str.split(".° ")
    for local,equipo in zip(octavos["Visitante"],locales):
        equipo_local = str(dict_grupos2022[equipo[1]].loc[dict_grupos2022[equipo[1]]["Pos"] == int(equipo[0]), "Selección"].values[0])
        octavos.replace(local,equipo_local,inplace=True)

    octavos

    # %%
    cuartos

    # %%
    ### Obtenemos ganadores de octavos y llenamos cuartos
    for partido,row in octavos.iterrows():
        ## Obtener ganador
        local = row["Local"]
        visitante = row["Visitante"]
        puntosLocal, puntosVisitante = 0,0
        while(puntosLocal == puntosVisitante):
            puntosLocal, puntosVisitante = Predecir_Puntos(local=local,visita=visitante)
        if(puntosLocal > puntosVisitante):
            ganador = local
        else:
            ganador = visitante
        
        #Actualizar cuartos
        cadena_cuartos = "Ganador " + row["Marcador"].lower()
        cuartos.replace(cadena_cuartos,ganador,inplace=True)

    cuartos

    # %%
    ### Mismo procedimiento con Semis
    for partido,row in cuartos.iterrows():
        ## Obtener ganador
        local = row["Local"]
        visitante = row["Visitante"]
        puntosLocal, puntosVisitante = 0,0
        while(puntosLocal == puntosVisitante):
            puntosLocal, puntosVisitante = Predecir_Puntos(local=local,visita=visitante)
        if(puntosLocal > puntosVisitante):
            ganador = local
        else:
            ganador = visitante
        
        #Actualizar cuartos
        cadena_semis = "Ganador " + row["Marcador"].lower()
        semis.replace(cadena_semis,ganador,inplace=True)

    semis

    # %%
    #Obtener partidos finales
    for partido,row in semis.iterrows():
        ## Obtener ganador
        local = row["Local"]
        visitante = row["Visitante"]
        puntosLocal, puntosVisitante = 0,0
        while(puntosLocal == puntosVisitante):
            puntosLocal, puntosVisitante = Predecir_Puntos(local=local,visita=visitante)
        if(puntosLocal > puntosVisitante):
            ganador = local
            perdedor = visitante
        else:
            ganador = visitante
            perdedor = local
        
        #Actualizar cuartos
        cadena_final = "Ganador " + row["Marcador"].lower()
        cadena_tercer = "Perdedor "+ row["Marcador"].lower()
        final.replace(cadena_final,ganador,inplace=True)
        tercer.replace(cadena_tercer,perdedor,inplace=True)


    # %%
    dict_bigfour = {}

    ganadores = []
    ### Tercer lugar
    for partido,row in tercer.iterrows():
        ## Obtener ganador
        local = row["Local"]
        visitante = row["Visitante"]
        puntosLocal, puntosVisitante = 0,0
        while(puntosLocal == puntosVisitante):
            puntosLocal, puntosVisitante = Predecir_Puntos(local=local,visita=visitante)
        if(puntosLocal > puntosVisitante):
            ganador = local
            perdedor = visitante
        else:
            ganador = visitante
            perdedor = local
        
        ganadores.append(perdedor)
        cuarto_lugar.append(perdedor)
        ganadores.append(ganador)
        tercer_lugar.append(ganador)

    ## Final
    for partido,row in final.iterrows():
        ## Obtener ganador
        local = row["Local"]
        visitante = row["Visitante"]
        puntosLocal, puntosVisitante = 0,0
        while(puntosLocal == puntosVisitante):
            puntosLocal, puntosVisitante = Predecir_Puntos(local=local,visita=visitante)
        if(puntosLocal > puntosVisitante):
            ganador = local
            perdedor = visitante
        else:
            ganador = visitante
            perdedor = local
        
        ganadores.append(perdedor)
        segundo_lugar.append(perdedor)
        ganadores.append(ganador)
        primer_lugar.append(ganador)

    dict_bigfour = {"Equipos":ganadores, "Posicion":[(4-i) for i in range(4)]}
    df_bigfour = pd.DataFrame(dict_bigfour)
    df_bigfour = df_bigfour.sort_values("Posicion")

dict_fullData = {"Primer Lugar":primer_lugar,"Segundo Lugar":segundo_lugar, "Tercer Lugar":tercer_lugar,"Cuarto Lugar":cuarto_lugar}
df_fullData = pd.DataFrame(dict_fullData)
df_fullData.to_csv("data/PredictComplete.csv")

