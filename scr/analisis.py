import matplotlib.pyplot as plt

def ventas_por_producto(df):
    print("\n📦 Ventas totales por producto:")
    resumen = df.groupby("Producto")["Total"].sum().sort_values(ascending=False)
    print(resumen)

    resumen.plot(kind="bar")
    plt.title("Ventas por Producto")
    plt.ylabel("Total ($)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig("ventas_por_producto.png")
    plt.show()

def mejores_clientes(df):
    clientes = df.groupby("Cliente")["Total"].sum().sort_values(ascending=False)
    print("\n🏆 Top 10 Mejores Clientes:")
    print(clientes.head(10))

    clientes.head(10).plot(kind="bar")
    plt.title("Top 10 Clientes")
    plt.ylabel("Total ($)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig("top_clientes.png")
    plt.show()

def analisis_por_categoria(df):
    print("\n" + "=" * 50)
    print("   📊 ANÁLISIS POR CATEGORÍA")
    print("=" * 50)

    for cat in df["Categoria"].unique():
        sub = df[df["Categoria"] == cat]
        cliente_top = sub.groupby("Cliente")["Total"].sum().sort_values(ascending=False)
        producto_top = sub.groupby("Producto")["Cantidad"].sum().sort_values(ascending=False)

        print(f"\n  Categoría: {cat}")
        print(f"   Cliente que más compra : {cliente_top.index[0]}  (${cliente_top.iloc[0]:,.2f})")
        print(f"   Producto más vendido   : {producto_top.index[0]}  ({producto_top.iloc[0]:,} unidades)")

    # Gráfica ventas por categoría
    ventas_cat = df.groupby("Categoria")["Total"].sum().sort_values(ascending=False)
    ventas_cat.plot(kind="bar", color=["#2196F3", "#4CAF50", "#FF9800"])
    plt.title("Ventas Totales por Categoría")
    plt.ylabel("Total ($)")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig("ventas_por_categoria.png")
    plt.show()
    print("\n📊 Gráfica guardada: ventas_por_categoria.png")

    # Gráfica detalle de la categoría principal
    cat_principal = df.groupby("Categoria")["Total"].sum().idxmax()
    sub_principal = df[df["Categoria"] == cat_principal]

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle(f"Detalle Categoría: {cat_principal}", fontsize=14, fontweight="bold")

    sub_principal.groupby("Cliente")["Total"].sum().sort_values(ascending=False).head(5).plot(
        kind="bar", ax=axes[0], color="#2196F3"
    )
    axes[0].set_title("Top 5 Clientes")
    axes[0].set_ylabel("Total ($)")
    axes[0].tick_params(axis="x", rotation=45)

    sub_principal.groupby("Producto")["Cantidad"].sum().sort_values(ascending=False).plot(
        kind="bar", ax=axes[1], color="#4CAF50"
    )
    axes[1].set_title("Productos más vendidos")
    axes[1].set_ylabel("Cantidad")
    axes[1].tick_params(axis="x", rotation=45)

    plt.tight_layout()
    plt.savefig("categoria_principal_detalle.png")
    plt.show()
    print("📊 Gráfica guardada: categoria_principal_detalle.png")