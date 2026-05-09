import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import NearestNeighbors

def entrenar_modelo(df, usar="Cantidad"):
    """
    Entrena KNN usando 'Cantidad' o 'Total' como métrica.
    usar: "Cantidad" | "Total"
    """
    print(f"\n Entrenando modelo ML (KNN) — métrica: {usar}...")

    le = LabelEncoder()
    df = df.copy()
    df["Producto_ID"] = le.fit_transform(df["Producto"])

    matriz = df.pivot_table(
        index="Cliente",
        columns="Producto_ID",
        values=usar,
        fill_value=0
    )

    modelo = NearestNeighbors(metric="cosine", n_neighbors=min(4, len(matriz)))
    modelo.fit(matriz)

    print(f" Modelo entrenado con {len(matriz)} clientes y {len(matriz.columns)} productos")
    return modelo, matriz, le

def graficar_ventas(df):
    ventas_producto = df.groupby("Producto")["Cantidad"].sum().sort_values(ascending=False)
    plt.figure()
    ventas_producto.plot(kind="bar", color="#2196F3")
    plt.title("Ventas totales por producto")
    plt.xlabel("Producto")
    plt.ylabel("Cantidad vendida")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig("ml_ventas_producto.png")
    plt.show()

    ventas_cliente = df.groupby("Cliente")["Cantidad"].sum().sort_values(ascending=False).head(10)
    plt.figure()
    ventas_cliente.plot(kind="bar", color="#4CAF50")
    plt.title("Top 10 clientes")
    plt.xlabel("Cliente")
    plt.ylabel("Cantidad comprada")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig("ml_top_clientes.png")
    plt.show()