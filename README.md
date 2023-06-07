# FIFA-WorldCup-Analyst
Un proyecto de análisis de datos de la copa de mundo donde predecimos el campeón de la copa del mundo de Qatar 2022. Simulamos desde la fase de grupos hasta la fase final.

## Metodología
Para poder realizar un modelo predictivo debemos obtener datos anteriores. Para esto realizamos web scrapping a todos los anteriores mundiales y obtenemos los resultados de cada equipo.
Almacenamos los goles anotados y recibidos por cada selección y los almacenamos en un archivo. Calculamos el promedio de los goles anotados y recibidos. 
Para predecir los resultados utilizamos la distribución de Poisson utilizando el promedio de goles y calculamos la probabilidad para ambos en equipos de anotar x cantidad de goles, que van desde 0 hasta 10.
Al final comparamos la suma de las probabilidades, el que tenga mayor gana el partido y si tienen las mismas quedan empate. En caso de equipos nuevos (como Qatar) le damos una probabilidad del 5% de que gane su partido.

## Resultados
Realizamos la simulación 1000 veces y obtuvimos que Brasil sería el campeón del mundo. El segundo lugar se reparte entre Francia, Argentina y Portugal. Y el tercer lugar se reparte entre Portugal, Argentina y Holanda.
          
