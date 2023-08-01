#SEGUNDO SCRIPT
# Se realiza una organización de las paradas en dependencia de su latitud por cada ruta existente

import pandas as pd

# Ruta del archivo Excel
archivo_excel = 'C:/Users/JesusPineda/Documents/SanuCorp/Trujillo/Rutas Grandes Trujillo.xlsx'

# Lee el archivo de Excel
dataframe = pd.read_excel(archivo_excel)

# Verifica si las columnas "Ruta" y "Latitud" existen en el DataFrame
if "Ruta" in dataframe.columns and "Latitud" in dataframe.columns:
    # Ordena los datos por la columna "Ruta" y "Latitud" de mayor a menor
    dataframe_ordenado = dataframe.sort_values(["Ruta", "Latitud"], ascending=[True, False])

    # Guarda el DataFrame ordenado en un nuevo archivo de Excel
    archivo_salida = 'C:/Users/JesusPineda/Documents/SanuCorp/Trujillo/Rutas Grandes Trujillo Ordenado.xlsx'
    dataframe_ordenado.to_excel(archivo_salida, index=False)

    print(f"Se ha ordenado el archivo Excel: {archivo_salida}")
else:
    print("No se encontró la columna de Ruta y/o Latitud en el archivo Excel.")
