#OPTIMIZADOR DE RUTA

# NECESITA QUE EL ARCHIVO QUE VA A SER USADO SOLO TENGA LOS DATOS DE UNA UNICA RUTA

#En este código, se utiliza un diccionario `matriz_distancias` para almacenar las distancias entre todas las combinaciones posibles de paradas. 
#Luego se utiliza la matriz de distancias en lugar de hacer solicitudes repetitivas a la API.

import googlemaps
import pandas as pd
import urllib.parse
from itertools import permutations
import time

# Inicia el temporizador
start_time = time.time()

# Ruta del archivo Excel
archivo_excel = 'C:/Users/JesusPineda/Documents/SanuCorp/Rutas Trujillo/Ruta 3 Trujillo.xlsx'

# Lee los datos del archivo Excel
datos_excel = pd.read_excel(archivo_excel)


# Obtiene las coordenadas de las paradas
paradas = [(fila['Latitud'], fila['Longitud']) for _, fila in datos_excel.iterrows()]

# Clave de la API de Google Maps
API_KEY = 'AIzaSyBiWx-pUsbjBAZ3iqQd8hvlHWvkoemx-0M'

# Crea un cliente de Google Maps
gmaps = googlemaps.Client(key=API_KEY)

# Calcula una matriz de distancias entre todas las paradas
matriz_distancias = {}
gmaps = googlemaps.Client(key=API_KEY)

for i in range(len(paradas)):
    for j in range(len(paradas)):
        origen = paradas[i]
        destino = paradas[j]
        
        ruta = gmaps.directions(
            origin=origen,
            destination=destino,
            mode='driving'
        )
        
        distancia = ruta[0]['legs'][0]['distance']['value']
        matriz_distancias[(i, j)] = distancia

# Obtiene todas las permutaciones posibles de las paradas
permutaciones = permutations(range(len(paradas)))

# Inicializa la mejor ruta y su distancia como infinito
mejor_ruta = None
mejor_distancia = float('inf')

# Calcula la distancia de cada permutación y encontrar la mejor ruta
for permutacion in permutaciones:
    distancia_total = 0
    
    # Calcula la distancia entre cada par de paradas en la permutación utilizando la matriz de distancias
    for i in range(len(permutacion)-1):
        origen = permutacion[i]
        destino = permutacion[i+1]
        
        distancia = matriz_distancias[(origen, destino)]
        distancia_total += distancia
    
    # Actualiza la mejor ruta y su distancia si la distancia actual es menor
    if distancia_total < mejor_distancia:
        mejor_ruta = permutacion
        mejor_distancia = distancia_total

# Obtiene el primer punto y último punto de la ruta optimizada
primer_punto = mejor_ruta[0]
ultimo_punto = mejor_ruta[-1]

# Obtiene las coordenadas del primer punto y último punto de la ruta optimizada
punto_origen = paradas[primer_punto]
punto_destino = paradas[ultimo_punto]

# Obtiene la ruta optimizada completa utilizando la API de Google Maps
ruta_optimizada = gmaps.directions(
    origin=punto_origen,
    destination=punto_destino,
    waypoints=[paradas[indice] for indice in mejor_ruta[1:-1]],
    mode='driving'
)

# Imprime los pasos de la ruta optimizada completa
pasos_ruta_optimizada = ruta_optimizada[0]['legs'][0]['steps']
print(f'Pasos de la ruta optimizada:')
for paso in pasos_ruta_optimizada:
    print(paso['html_instructions'])
print()

# Imprime la duración de la ruta optimizada
duracion_optimizada = ruta_optimizada[0]['legs'][0]['duration']['text']
print(f'Tiempo estimado de la ruta optimizada: {duracion_optimizada}')

# Muestra el mapa interactivo con la ruta optimizada trazada
url_paradas = "|".join([urllib.parse.quote(f'{paradas[indice][0]},{paradas[indice][1]}') for indice in mejor_ruta])
url_mapa = f'https://www.google.com/maps/dir/?api=1&waypoints={url_paradas}&travelmode=driving'
print("URL del mapa:", url_mapa)

# Fin del temporizador
end_time = time.time()

# Calcula el tiempo total de ejecución
tiempo_ejecucion = end_time - start_time

# Imprime el tiempo de ejecución en segundos y en formato legible
print(f'\nTiempo de ejecución del código: {tiempo_ejecucion:.2f} segundos')
