# PRIMER SCRIPT
# Se toma el archivo de excel compartido por el cliente y se asignan rutas iniciales con gran cantidad de paradas asignadas por zonas del mapa

import pandas as pd
import math
from sklearn.cluster import KMeans

# Ruta del archivo Excel
archivo_excel = 'C:/Users/JesusPineda/Documents/SanuCorp/Copy of Trujillo (003).xlsx'

# Lee el archivo de Excel
dataframe = pd.read_excel(archivo_excel)

# Filtra los registros con valores faltantes en las columnas Latitud y Longitud
dataframe = dataframe.dropna(subset=['Latitud', 'Longitud'])

# Obtén las coordenadas de los lugares existentes
coordenadas = dataframe[['Latitud', 'Longitud']].values

# Define el número máximo de datos por grupo
max_datos_por_grupo = 16

# Calcula el número de clústeres basado en el número máximo de datos por grupo
n_clusters = math.ceil(len(coordenadas) / max_datos_por_grupo)

# Aplica el algoritmo de clustering de K-means con el número de clústeres calculado
kmeans = KMeans(n_clusters=n_clusters)
kmeans.fit(coordenadas)

# Obtiene las etiquetas de los grupos
etiquetas = kmeans.labels_

# Asigna los grupos a las etiquetas de grupo en el DataFrame
dataframe['Ruta'] = etiquetas + 1

# Verifica si hay grupos con más de max_datos_por_grupo datos y ajusta los grupos
for grupo in range(1, n_clusters + 1):
    grupo_actual = dataframe[dataframe['Ruta'] == grupo]
    num_datos_grupo_actual = len(grupo_actual)
    
    if num_datos_grupo_actual > max_datos_por_grupo:
        datos_sobrantes = grupo_actual.sample(num_datos_grupo_actual - max_datos_por_grupo)
        
        for index, row in datos_sobrantes.iterrows():
            grupo_cercano = kmeans.predict([row[['Latitud', 'Longitud']]])[0]
            dataframe.loc[index, 'Ruta'] = grupo_cercano + 1

# Ordena el DataFrame por el número de grupo de manera ascendente
dataframe_ordenado = dataframe.sort_values(by='Ruta')

# Genera el nombre del archivo de Excel para guardar los resultados
nombre_archivo = 'C:/Users/JesusPineda/Documents/SanuCorp/Trujillo/Rutas Grandes Trujillo.xlsx'

# Exporta el DataFrame ordenado a un nuevo archivo de Excel
dataframe_ordenado.to_excel(nombre_archivo, index=False)

print("El análisis de coordenadas y la asignación de grupos han sido completados.")
print(f"Los resultados han sido guardados en el archivo '{nombre_archivo}'.")
print(f"Cada Ruta contiene un máximo de {max_datos_por_grupo} datos o menos.")
