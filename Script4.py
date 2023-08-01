# CUARTO SCRIPT
# Hace una sumatoria de los pesos por cada ruta y si es mayor a 4.8, toma la última fila de la ruta y la envia a formar parte de la siguiente ruta

import pandas as pd

# Lee el archivo de Excel
df = pd.read_excel('C:/Users/JesusPineda/Documents/SanuCorp/Trujillo/Rutas Trujillo Ordenado.xlsx')

# Ordena el dataframe por ruta, subruta en orden ascendente
df.sort_values(by=['Ruta', 'Subruta'], ascending=True, inplace=True)

# Crea una variable para controlar el bucle
hay_modificaciones = True

# Repite el código hasta que no haya modificaciones
while hay_modificaciones:
    # Calcula la sumatoria por cada subruta
    sumatorias = df.groupby(['Ruta', 'Subruta'])['Total(TM/Quincenal)'].sum()

    # Crea una lista para almacenar las filas a modificar
    filas_modificar = []

    # Recorre las sumatorias y marcar la última fila de la subruta a mover
    for (ruta, subruta), sumatoria in sumatorias.items():
        if sumatoria > 4.8:
            filas_subruta = df[(df['Ruta'] == ruta) & (df['Subruta'] == subruta)].index
            filas_modificar.append(filas_subruta[-1])

    # Sale del bucle si no hay filas a modificar
    if len(filas_modificar) == 0:
        hay_modificaciones = False
        break

    # Cambia el valor de la casilla subruta por el valor de la siguiente subruta dentro de la misma ruta
    for fila in filas_modificar:
        ruta_actual = df.loc[fila, 'Ruta']
        subruta_actual = df.loc[fila, 'Subruta']
        filas_siguiente_subruta = df[(df['Ruta'] == ruta_actual) & (df['Subruta'] > subruta_actual)].index
        if len(filas_siguiente_subruta) > 0:
            subruta_siguiente = df.loc[filas_siguiente_subruta[0], 'Subruta']
            df.loc[fila, 'Subruta'] = subruta_siguiente

# Guarda el dataframe modificado en un nuevo archivo
df.to_excel('C:/Users/JesusPineda/Documents/SanuCorp/Trujillo/Rutas Trujillo.xlsx', index=False)

