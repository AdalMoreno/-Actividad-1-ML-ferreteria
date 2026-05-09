from load_data import cargar_datos
from procesamiento import limpiar_datos
from analisis import ventas_por_producto, mejores_clientes, analisis_por_categoria
from model_ML import entrenar_modelo, graficar_ventas
from recomendacion import recomendar


def menu():
    print("\n" + "=" * 45)
    print("   SISTEMA DE ANÁLISIS DE FERRETERÍA")
    print("=" * 45)
    print("  1. Cargar y limpiar datos")
    print("  2. Ventas por producto")
    print("  3. Top 10 mejores clientes")
    print("  4. Entrenar modelo ML + gráficas")
    print("  5. Recomendar productos a un cliente")
    print("  6. Ejecutar todo automáticamente")
    print("  7. Analisis por categoria")
    print("  8. Reporte del maestro")
    print("  0. Salir")
    print("=" * 45)
    return input("  Elige una opción: ").strip()


def main():
    df_limpio = None
    modelo = None
    matriz = None
    le = None

    while True:
        opcion = menu()

        # ── 1. Cargar datos ──────────────────────────
        if opcion == "1":
            df_raw = cargar_datos()
            df_limpio = limpiar_datos(df_raw)

        # ── 2. Ventas por producto ───────────────────
        elif opcion == "2":
            if df_limpio is None:
                print("  Primero carga los datos (opción 1).")
            else:
                ventas_por_producto(df_limpio)

        # ── 3. Mejores clientes ──────────────────────
        elif opcion == "3":
            if df_limpio is None:
                print("  Primero carga los datos (opción 1).")
            else:
                mejores_clientes(df_limpio)

        # ── 4. Modelo ML ─────────────────────────────
        elif opcion == "4":
            if df_limpio is None:
                print("  Primero carga los datos (opción 1).")
            else:
                modelo, matriz, le = entrenar_modelo(df_limpio)
                graficar_ventas(df_limpio)

        # ── 5. Recomendaciones ───────────────────────
        elif opcion == "5":
            if modelo is None:
                print("  Primero entrena el modelo (opción 4).")
            else:
                cliente = input("\n  Ingresa el nombre del cliente: ").strip()
                productos = recomendar(cliente, modelo, matriz, le)
                if productos:
                    print(f"\n Productos recomendados para {cliente}:")
                    for i, p in enumerate(productos, 1):
                        print(f"   {i}. {p}")
                else:
                    print("  No se encontraron recomendaciones.")

        # ── 6. Todo automático ───────────────────────
        elif opcion == "6":
            print("\n Ejecutando análisis completo...\n")

            df_raw = cargar_datos()
            df_limpio = limpiar_datos(df_raw)

            ventas_por_producto(df_limpio)
            mejores_clientes(df_limpio)

            modelo, matriz, le = entrenar_modelo(df_limpio)
            graficar_ventas(df_limpio)

            primer_cliente = matriz.index[0]
            print(f"\n Ejemplo de recomendación para: {primer_cliente}")
            productos = recomendar(primer_cliente, modelo, matriz, le)
            if productos:
                for i, p in enumerate(productos, 1):
                    print(f"   {i}. {p}")

            print("\n Análisis completo terminado.")

        # ── 7. Análisis por categoría ─────────────────
        elif opcion == "7":
            if df_limpio is None:
                print("  Primero carga los datos (opción 1).")
            else:
                analisis_por_categoria(df_limpio)

        # ── 8. Reporte del maestro ────────────────────
        elif opcion == "8":
            if modelo is None:
                print("  Primero entrena el modelo (opción 4).")
            else:
                import importlib
                import reporte
                importlib.reload(reporte)

        # ── 0. Salir ─────────────────────────────────
        elif opcion == "0":
            print("\n Hasta luego!\n")
            break

        else:
            print(" Opción no válida, intenta de nuevo.")


if __name__ == "__main__":
    main()