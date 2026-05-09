
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from load_data import cargar_datos
from procesamiento import limpiar_datos
from model_ML import entrenar_modelo
from recomendacion import recomendar

df = cargar_datos()
df = limpiar_datos(df)

import matplotlib.pyplot as plt

print("\n" + "=" * 55)
print("     ANÁLISIS POR CATEGORÍA")
print("=" * 55)

for cat in df["Categoria"].unique():
    sub = df[df["Categoria"] == cat]
    cliente_top  = sub.groupby("Cliente")["Total"].sum().sort_values(ascending=False)
    producto_top = sub.groupby("Producto")["Cantidad"].sum().sort_values(ascending=False)

    print(f"\n  {cat}")
    print(f"    Cliente que más compra : {cliente_top.index[0]}  (${cliente_top.iloc[0]:,.2f})")
    print(f"    Producto más vendido   : {producto_top.index[0]}  ({producto_top.iloc[0]:,} unidades)")

# Gráfica por categoría
ventas_cat = df.groupby("Categoria")["Total"].sum().sort_values(ascending=False)
ventas_cat.plot(kind="bar", color=["#2196F3", "#4CAF50", "#FF9800"])
plt.title("Ventas Totales por Categoría")
plt.ylabel("Total ($)")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig("reporte_categoria.png")
plt.show()
print("\n Gráfica guardada: reporte_categoria.png")


print("\n" + "=" * 55)
print("    MODELO ML (entrenado con Total $)")
print("=" * 55)

modelo, matriz, le = entrenar_modelo(df, usar="Total")

# Gráfica ventas por producto y top clientes
ventas_prod = df.groupby("Producto")["Total"].sum().sort_values(ascending=False)
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("Modelo ML — Análisis por Total $", fontsize=13, fontweight="bold")

ventas_prod.plot(kind="bar", ax=axes[0], color="#2196F3")
axes[0].set_title("Ventas por Producto ($)")
axes[0].set_ylabel("Total ($)")
axes[0].tick_params(axis="x", rotation=45)

df.groupby("Cliente")["Total"].sum().sort_values(ascending=False).head(10).plot(
    kind="bar", ax=axes[1], color="#9C27B0"
)
axes[1].set_title("Top 10 Clientes ($)")
axes[1].set_ylabel("Total ($)")
axes[1].tick_params(axis="x", rotation=45)

plt.tight_layout()
plt.savefig("reporte_ml_total.png")
plt.show()
print(" Gráfica guardada: reporte_ml_total.png")


print("\n" + "=" * 55)
print("     REPORTE DEL MAESTRO")
print("=" * 55)

# Producto más vendido
producto_top = df.groupby("Producto")["Cantidad"].sum().sort_values(ascending=False)
print(f"\n PRODUCTO MÁS VENDIDO")
print(f"   {producto_top.index[0]}  →  {producto_top.iloc[0]:,} unidades")

# Cliente más top
cliente_rank = df.groupby("Cliente")["Total"].sum().sort_values(ascending=False)
print(f"\n CLIENTE MÁS TOP")
print(f"   {cliente_rank.index[0]}  →  ${cliente_rank.iloc[0]:,.2f} en compras totales")

# Categoría más importante
cat_rank = df.groupby("Categoria")["Total"].sum().sort_values(ascending=False)
print(f"\n CATEGORÍA MÁS IMPORTANTE")
print(f"   {cat_rank.index[0]}  →  ${cat_rank.iloc[0]:,.2f} en ventas")

# Tres clientes potenciales (los siguientes 3 después del #1)
potenciales = cliente_rank.index[1:4].tolist()
print(f"\n TRES CLIENTES POTENCIALES")
for i, c in enumerate(potenciales, 1):
    print(f"   {i}. {c}  →  ${cliente_rank[c]:,.2f}")

# Recomendación personalizada para cada uno
print(f"\n RECOMENDACIONES PERSONALIZADAS")
print("-" * 55)
for cliente in potenciales:
    productos = recomendar(cliente, modelo, matriz, le, top_n=3)
    print(f"\n   {cliente}")
    if productos:
        print(f"     Sugerencias basadas en clientes similares:")
        for i, p in enumerate(productos, 1):
            print(f"       {i}. {p}")
    else:
        cat_fav = df[df["Cliente"] == cliente].groupby("Categoria")["Total"].sum().idxmax()
        prod_fav = df[df["Categoria"] == cat_fav].groupby("Producto")["Cantidad"].sum().idxmax()
        print(f"     Ya compra toda la variedad.")
        print(f"     Reforzar: {prod_fav} en categoría {cat_fav}")

print("\n" + "=" * 55)
print("   REPORTE COMPLETO TERMINADO")
print("=" * 55)