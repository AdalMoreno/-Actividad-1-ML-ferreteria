import pandas as pd
import os

def cargar_datos():
    ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "ventas.xlsx")
    df = pd.read_excel(ruta)
    print("\n Primeros registros:")
    print(df.head())
    print("\nℹ  Información del dataset:")
    print(df.info())
    return df