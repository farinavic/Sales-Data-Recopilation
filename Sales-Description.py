import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Cargar datos de facturas
facturas = pd.read_csv('facturas_articulos1.csv')

# Cargar datos de promociones
promociones = pd.read_csv('PromosVigentesSemana.csv')


#facturas['semana'] = pd.to_datetime(facturas['fecha'], format='%Y-%m-%d').dt.isocalendar().week

#Crea columnas de parametro
promociones['fecha_7_antes'] = pd.to_datetime(promociones['fecha_inicio']) - pd.DateOffset(days=7)
promociones['fecha_14_antes'] = pd.to_datetime(promociones['fecha_7_antes']) - pd.DateOffset(days=7)
promociones['fecha_7_despues'] = pd.to_datetime(promociones['fecha_fin']) + pd.DateOffset(days=7)
promociones['fecha_14_despues'] = pd.to_datetime(promociones['fecha_7_despues']) + pd.DateOffset(days=7)
print(promociones)

# Convertir las fechas a formato datetime
facturas['fecha'] = pd.to_datetime(facturas['fecha'], format='%Y-%m-%d').dt.strftime('%d-%m-%Y')
promociones['fecha_inicio'] = pd.to_datetime(promociones['fecha_inicio'], format='%d/%m/%Y').dt.strftime('%d-%m-%Y')
promociones['fecha_fin'] = pd.to_datetime(promociones['fecha_fin'], format='%d/%m/%Y').dt.strftime('%d-%m-%Y')

promociones['fecha_7_antes'] = pd.to_datetime(promociones['fecha_inicio'], format='%d-%m-%Y').dt.strftime('%d-%m-%Y')
promociones['fecha_14_antes'] = pd.to_datetime(promociones['fecha_7_antes'], format='%d-%m-%Y').dt.strftime('%d-%m-%Y')
promociones['fecha_7_despues'] = pd.to_datetime(promociones['fecha_fin'], format='%d-%m-%Y').dt.strftime('%d-%m-%Y')
promociones['fecha_14_despues'] = pd.to_datetime(promociones['fecha_7_despues'], format='%d-%m-%Y').dt.strftime('%d-%m-%Y')


#Creacion Dfs para analizar
facturas_en_promocion = pd.DataFrame()
facturas_7_antes= pd.DataFrame()
facturas_14_antes= pd.DataFrame()
facturas_7_despues= pd.DataFrame()
facturas_14_despues= pd.DataFrame()

for index_promo, row_promo in promociones.iterrows():
    for index_factura, row_factura in facturas.iterrows():
        #Crea Df facturas en promocion
        if (
            (row_factura['codigo_articulo'] == row_promo['codigo_articulo']) and
            (row_factura['fecha'] >= row_promo['fecha_inicio']) and
            (row_factura['fecha'] <= row_promo['fecha_fin'])
            
        ):
            facturas_en_promocion = pd.concat([facturas_en_promocion, pd.DataFrame([row_factura])])
        #Crea Df facturas 7 dias antes de promocion
        if (
            (row_factura['codigo_articulo'] == row_promo['codigo_articulo']) and
            (row_factura['fecha'] >= row_promo['fecha_7_antes']) and
            (row_factura['fecha'] <= row_promo['fecha_inicio'])
            
        ):
            facturas_7_antes = pd.concat([facturas_7_antes, pd.DataFrame([row_factura])])
        #Crea Df facturas 14 dias antes de promocion
        if (
            (row_factura['codigo_articulo'] == row_promo['codigo_articulo']) and
            (row_factura['fecha'] >= row_promo['fecha_14_antes']) and
            (row_factura['fecha'] <= row_promo['fecha_7_antes'])
            
        ):
            facturas_14_antes = pd.concat([facturas_14_antes, pd.DataFrame([row_factura])])
        #Crea Df facturas 7 dias despues de promocion
        if (
            (row_factura['codigo_articulo'] == row_promo['codigo_articulo']) and
            (row_factura['fecha'] >= row_promo['fecha_fin']) and
            (row_factura['fecha'] <= row_promo['fecha_7_despues'])
            
        ):
            facturas_7_despues = pd.concat([facturas_7_despues, pd.DataFrame([row_factura])])
        #Crea Df facturas 14 dias despues de promocion
        if (
            (row_factura['codigo_articulo'] == row_promo['codigo_articulo']) and
            (row_factura['fecha'] >= row_promo['fecha_7_despues']) and
            (row_factura['fecha'] <= row_promo['fecha_14_despues'])
            
        ):
            facturas_14_despues = pd.concat([facturas_14_despues, pd.DataFrame([row_factura])])
    

# Reinicia los índices del DataFrame resultante

# Imprimir las facturas que se hicieron durante alguna promoción

def guardar_como_csv(dataframe, nombre_archivo):
    """
    Guarda un DataFrame como un archivo CSV en la misma carpeta que el script.
    
    Parameters:
        dataframe (pd.DataFrame): El DataFrame que se va a guardar.
        nombre_archivo (str): El nombre del archivo CSV.
   """
    ruta = os.path.join(os.path.dirname(_file_), nombre_archivo)
    dataframe.to_csv(ruta, index=False)
    print(f"Se ha guardado '{nombre_archivo}' en la carpeta del script.")

# Guardar cada DataFrame con su nombre respectivo
guardar_como_csv(facturas_en_promocion, 'facturas_en_promocion.csv')
guardar_como_csv(facturas_7_antes, 'facturas_7_antes.csv')
guardar_como_csv(facturas_14_antes, 'facturas_14_antes.csv')
guardar_como_csv(facturas_7_despues, 'facturas_7_despues.csv')
guardar_como_csv(facturas_14_despues, 'facturas_14_despues.csv')
