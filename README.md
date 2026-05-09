#  Análisis de Ventas — Ferretería

Proyecto en Python que analiza las ventas de una ferretería. Limpia los datos, genera gráficas y usa Machine Learning para recomendar productos a los mejores clientes.

## ¿Qué hace?

- Carga y limpia el archivo de ventas en Excel
- Muestra las ventas por producto, cliente y categoría
- Entrena un modelo KNN para encontrar clientes similares
- Recomienda productos personalizados a cada cliente
- Genera un reporte con los indicadores clave del negocio

## Estructura

```
FERRETERIA/
├── data/
│   └── ventas.xlsx
└── scr/
    ├── main.py              # Menú principal
    ├── reporte.py           # Reporte completo
    ├── load_data.py         # Carga del Excel
    ├── procesamiento.py     # Limpieza de datos
    ├── analisis.py          # Gráficas y estadísticas
    ├── model_ML.py          # Modelo KNN
    └── recomendacion.py     # Recomendaciones por cliente
```

## Cómo ejecutarlo

```bash
pip install pandas openpyxl matplotlib scikit-learn
cd scr
python main.py
```

## Resultados

| Indicador | Resultado |
|-----------|-----------|
| Producto más vendido | Martillo — 3,457 unidades |
| Cliente más top | Cliente_9 — $169,437.52 |
| Categoría más importante | Herramientas — $5,380,235.90 |

## Tecnologías

Python · pandas · matplotlib · scikit-learn
