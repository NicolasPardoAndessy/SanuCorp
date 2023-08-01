# TERCER SCRIPT
# Se cambia el nombre de la columna que almacena la carga que debe ser transportada quicenalmente
# Identifica las rutas iniciales cuya cantidad de paradas es mayor a 9 y las divide en subrutas con casi la misma cantidad de paradas (impares)


import pandas as pd
import numpy as np
from openpyxl import load_workbook

# Cargar archivo de Excel
workbook = load_workbook(filename="C:/Users/JesusPineda/Documents/SanuCorp/Trujillo/Rutas Grandes Trujillo Ordenado.xlsx")
sheet = workbook.active

# Modificar la celda deseada
sheet["I1"] = "Total(TM/Quincenal)"

# Guardar el archivo
workbook.save(filename="C:/Users/JesusPineda/Documents/SanuCorp/Trujillo/Rutas Grandes Trujillo Ordenado.xlsx")

def dividir_rutas(archivo_excel, columna_ruta):
    # Leer el archivo de Excel
    df = pd.read_excel(archivo_excel)
    
    # Crear una nueva columna llamada "Subruta"
    df['Subruta'] = ''
    
    # Obtener las rutas con más de 10 integrantes
    rutas_mas_9_integrantes = df[columna_ruta].value_counts().loc[lambda x: x > 9].index
    
    # Iterar sobre cada ruta con más de 10 integrantes
    for ruta in rutas_mas_9_integrantes:
        # Filtrar el dataframe por la ruta actual
        df_ruta = df[df[columna_ruta] == ruta]
        
        # Obtener la cantidad de integrantes en la ruta actual
        cantidad_integrantes = df_ruta.shape[0]
        
        # Calcular la cantidad de subrutas necesarias
        cantidad_subrutas = cantidad_integrantes // 9
        if cantidad_integrantes % 9 != 0:
            cantidad_subrutas += 1
        
        # Dividir la ruta en subrutas
        subrutas = np.array_split(df_ruta, cantidad_subrutas)
        
        # Asignar el nombre de la subruta a cada subruta
        for i, subruta in enumerate(subrutas):
            subruta_actual = i + 1
            subruta['Subruta'] = subruta_actual
        
        # Concatenar las subrutas en un nuevo dataframe
        df_subrutas = pd.concat(subrutas)
        
        # Actualizar el dataframe original con los datos de las subrutas
        df.update(df_subrutas)
    
    # Reiniciar la numeración de todas las rutas (incluyendo las subrutas)
    df['RUTAS'] = df.groupby(['Ruta', 'Subruta']).ngroup() + 1
    
    return df

def sumar_por_subgrupos(archivo_excel):
    # Leer el archivo de Excel
    df = pd.read_excel(archivo_excel)
    
    # Calcular la sumatoria por subgrupos
    df_suma = df.groupby(['Ruta', 'Subruta'])['Total(TM/Quincenal)'].sum().reset_index()
    
    # Imprimir la sumatoria por subgrupos en pantalla
    print(df_suma)

# Archivo de uso
archivo_excel = 'C:/Users/JesusPineda/Documents/SanuCorp/Trujillo/Rutas Grandes Trujillo Ordenado.xlsx'
columna_ruta = 'Ruta'

df = dividir_rutas(archivo_excel, columna_ruta)

# Guardar el dataframe en un nuevo archivo de Excel
df.to_excel('C:/Users/JesusPineda/Documents/SanuCorp/Trujillo/Rutas Trujillo Ordenado.xlsx', index=False)
