# Marketing & Growth Analytics — Customer Personality Analysis

Proyecto de portfolio de analítica de marketing/growth: partiendo de un dataset real de Kaggle, el objetivo es limpiar y modelar los datos, construir un dashboard en **Power BI** y, finalmente, un **dashboard interactivo en HTML** que explique los insights clave y el "so what" para el negocio (qué debería hacer una empresa con esta información).

## Objetivo del proyecto

Responder, desde una perspectiva de marketing/growth, preguntas como:

- ¿Qué campañas de marketing funcionan mejor y con qué tipo de cliente?
- ¿Qué canal de compra (web, catálogo, tienda física) genera más ingresos y por qué segmento?
- ¿Qué perfil de cliente (renta, edad, hijos, educación) tiene mayor propensión a responder a campañas?
- ¿Dónde hay oportunidades de crecimiento (upsell, cross-sell, retención) según el comportamiento de compra?

La meta no es solo describir los datos, sino traducirlos en **recomendaciones accionables** para un equipo de marketing/growth.

## Dataset

**[Customer Personality Analysis](https://www.kaggle.com/datasets/rodsaldanha/arketing-campaign)** (Kaggle, autor: rodsaldanha)

Elegido porque:
- Es un único CSV, ~2.240 filas, sin necesidad de cruzar tablas — fácil de limpiar y modelar rápido.
- Combina datos demográficos, comportamiento de compra por canal y respuesta a campañas de marketing en el mismo dataset, lo que permite análisis de growth (conversión, segmentación, canal) sin depender de fuentes externas.
- Es uno de los datasets de marketing más usados como referencia en proyectos de Power BI/Tableau, por lo que hay mucho contexto y buenas prácticas documentadas.

### Diccionario de datos (resumen)

| Columna | Descripción |
|---|---|
| `ID` | Identificador único de cliente |
| `Year_Birth` | Año de nacimiento |
| `Education` | Nivel educativo |
| `Marital_Status` | Estado civil |
| `Income` | Ingresos anuales del hogar |
| `Kidhome` / `Teenhome` | Nº de niños / adolescentes en el hogar |
| `Dt_Customer` | Fecha de alta como cliente |
| `Recency` | Días desde la última compra |
| `MntWines`, `MntFruits`, `MntMeatProducts`, `MntFishProducts`, `MntSweetProducts`, `MntGoldProds` | Gasto (últimos 2 años) por categoría de producto |
| `NumDealsPurchases` | Compras hechas con descuento |
| `NumWebPurchases`, `NumCatalogPurchases`, `NumStorePurchases` | Compras por canal |
| `NumWebVisitsMonth` | Visitas a la web/mes |
| `AcceptedCmp1`–`AcceptedCmp5` | Si aceptó la campaña 1 a 5 (1/0) |
| `Response` | Si aceptó la última campaña (1/0) |
| `Complain` | Si presentó una queja en los últimos 2 años |

## Roadmap del proyecto

- [x] Selección del dataset y definición del objetivo de negocio
- [x] Limpieza y preparación de datos (`data/`)
- [ ] Dashboard en Power BI (`powerbi/`) — guía de construcción lista, `.pbix` pendiente de subir
- [ ] Dashboard interactivo en HTML con insights y "so what" (`dashboard/`)

## Estructura del repositorio

```
data/       # Dataset (crudo y procesado) — ver data/README.md para cómo obtenerlo
powerbi/    # Archivo .pbix y documentación del modelo/medidas DAX
dashboard/  # Dashboard HTML interactivo con los insights finales
```

## Cómo obtener los datos

El dataset no se incluye en este repositorio (requiere login en Kaggle para su descarga). Instrucciones en [`data/README.md`](data/README.md).

## Stack

- Python / pandas para limpieza y preparación de datos
- Power BI para el análisis exploratorio y el dashboard de negocio
- HTML/CSS/JS para el dashboard interactivo final con los insights
