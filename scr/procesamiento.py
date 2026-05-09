import pandas as pd

def limpiar_datos(df):
    print("\n Valores nulos encontrados:")
    print(df.isnull().sum())

    df = df.dropna()
    df["Fecha"] = pd.to_datetime(df["Fecha"])
    df = df[df["Cantidad"] > 0]
    df = df[df["Precio_Unitario"] > 0]

    print(f"\n Datos limpios: {len(df)} registros válidos")
    return df