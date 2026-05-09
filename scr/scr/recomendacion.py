def recomendar(cliente, modelo, matriz, le, top_n=3):
    if cliente not in matriz.index:
        print(f"  Cliente '{cliente}' no existe en la base de datos.")
        return []

    vector = matriz.loc[cliente].values.reshape(1, -1)
    distancia, indices = modelo.kneighbors(vector, n_neighbors=top_n + 1)

    vecinos = matriz.index[indices.flatten()[1:]]
    recomendaciones = matriz.loc[vecinos].mean().sort_values(ascending=False)

    # Filtrar productos que el cliente ya compró
    ya_comprados = set(matriz.columns[matriz.loc[cliente] > 0])
    recomendaciones = recomendaciones[~recomendaciones.index.isin(ya_comprados)]

    # Si ya compró todo, recomendar los que menos ha comprado
    if len(recomendaciones) == 0:
        recomendaciones = matriz.loc[cliente].sort_values(ascending=True)

    productos = le.inverse_transform(recomendaciones.index[:top_n].astype(int))
    return list(productos)


def reporte_maestro(df, modelo, matriz, le):
    print("\n" + "=" * 55)
    print("         REPORTE FINAL — ANÁLISIS DE VENTAS")
    print("=" * 55)

    # Producto más vendido
    producto_top = df.groupby("Producto")["Cantidad"].sum().sort_values(ascending=False)
    print(f"\n PRODUCTO MAS VENDIDO")
    print(f"   {producto_top.index[0]}  ->  {producto_top.iloc[0]:,} unidades vendidas")

    # Cliente más top
    cliente_rank = df.groupby("Cliente")["Total"].sum().sort_values(ascending=False)
    print(f"\n CLIENTE MAS TOP")
    print(f"   {cliente_rank.index[0]}  ->  ${cliente_rank.iloc[0]:,.2f} en compras totales")

    # Categoría más importante
    cat_rank = df.groupby("Categoria")["Total"].sum().sort_values(ascending=False)
    print(f"\n CATEGORIA MAS IMPORTANTE")
    print(f"   {cat_rank.index[0]}  ->  ${cat_rank.iloc[0]:,.2f} en ventas")

    # Tres clientes potenciales
    potenciales = cliente_rank.index[1:4].tolist()
    print(f"\n TRES CLIENTES POTENCIALES")
    for i, c in enumerate(potenciales, 1):
        print(f"   {i}. {c}  ->  ${cliente_rank[c]:,.2f}")

    # Recomendación personalizada
    print(f"\n RECOMENDACIONES PERSONALIZADAS")
    print("-" * 55)
    for cliente in potenciales:
        productos = recomendar(cliente, modelo, matriz, le, top_n=3)
        compras = matriz.loc[cliente].sort_values(ascending=True)
        print(f"\n  {cliente}")
        print(f"  Productos que menos ha comprado (oportunidad de venta):")
        for i, p in enumerate(productos, 1):
            cantidad = int(matriz.loc[cliente, le.transform([p])[0]])
            print(f"    {i}. {p}  ({cantidad} unidades compradas hasta ahora)")

    print("\n" + "=" * 55)