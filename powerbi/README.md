# Guía Power BI

Guía para construir el dashboard de Power BI a partir de `data/processed/marketing_campaign_clean.csv`, alineada con las preguntas de negocio del README principal.

## 1. Importar los datos

1. Power BI Desktop → **Get Data → Text/CSV** → selecciona `marketing_campaign_clean.csv`.
2. Revisa los tipos de dato al cargar: `Dt_Customer` debe quedar como **Fecha**, `ID` como **Número entero**, el resto de `Mnt*`/`Num*` como **Número entero**, `Income`/`Total_Spend` como **Decimal**.
3. Marca `Dt_Customer` como columna de fecha para poder usar inteligencia de tiempo (clic derecho en la tabla → **Mark as date table**, o crea una tabla de calendario aparte si prefieres).

## 2. Transformaciones en Power Query (recomendadas)

La tabla viene "ancha" (una columna por canal/categoría/campaña). Para poder graficar "por canal" o "por categoría" con una sola serie, conviene crear 3 tablas auxiliares **referenciando** la tabla principal y usando **Unpivot columns**:

- **Channel** (referencia la tabla principal, quédate solo con `ID` + `NumDealsPurchases`, `NumWebPurchases`, `NumCatalogPurchases`, `NumStorePurchases` → Unpivot esas 4 columnas → renombra a `Channel` / `Purchases`).
- **Category** (igual pero con `MntWines`, `MntFruits`, `MntMeatProducts`, `MntFishProducts`, `MntSweetProducts`, `MntGoldProds` → `Category` / `Spend`).
- **Campaign** (igual con `AcceptedCmp1-5` + `Response` → `Campaign` / `Accepted`).

Esto te permitirá hacer gráficos de barras "por canal" o "por categoría" sin tener que crear una medida por columna.

## 3. Columnas calculadas útiles (en la tabla principal)

```dax
Spend Tier =
SWITCH(
    TRUE(),
    marketing_campaign_clean[Total_Spend] <= 69, "Low",
    marketing_campaign_clean[Total_Spend] <= 396, "Medium",
    marketing_campaign_clean[Total_Spend] <= 1045, "High",
    "Top"
)

Age Group =
SWITCH(
    TRUE(),
    marketing_campaign_clean[Age] < 30, "18-29",
    marketing_campaign_clean[Age] < 45, "30-44",
    marketing_campaign_clean[Age] < 60, "45-59",
    "60+"
)

Has Children = IF(marketing_campaign_clean[Kidhome] + marketing_campaign_clean[Teenhome] > 0, "Con hijos", "Sin hijos")
```

(Los cortes de `Spend Tier` son los cuartiles reales del dataset limpio — puedes ajustarlos si lo prefieres.)

## 4. Medidas DAX clave

```dax
Total Customers = DISTINCTCOUNT(marketing_campaign_clean[ID])

Total Revenue = SUM(marketing_campaign_clean[Total_Spend])

Avg Customer Value = DIVIDE([Total Revenue], [Total Customers])

Avg Income = AVERAGE(marketing_campaign_clean[Income])

Avg Recency = AVERAGE(marketing_campaign_clean[Recency])

Campaign Response Rate = DIVIDE(SUM(marketing_campaign_clean[Response]), [Total Customers])

Complaint Rate = DIVIDE(SUM(marketing_campaign_clean[Complain]), [Total Customers])

% Multi-Campaign Responders =
DIVIDE(
    CALCULATE([Total Customers], marketing_campaign_clean[Total_Campaigns_Accepted] >= 2),
    [Total Customers]
)

Web Conversion Proxy = DIVIDE(SUM(marketing_campaign_clean[NumWebPurchases]), SUM(marketing_campaign_clean[NumWebVisitsMonth]))
```

Si usas la tabla `Campaign` (unpivoted), la tasa de aceptación por campaña sale directa con una medida:

```dax
Campaign Acceptance Rate = DIVIDE(SUM(Campaign[Accepted]), DISTINCTCOUNT(Campaign[ID]))
```
— y la desglosas por campaña simplemente poniendo `Campaign[Campaign]` como eje del gráfico.

## 5. Páginas sugeridas del dashboard

**Página 1 — Overview**
KPIs (tarjetas): Total Customers, Total Revenue, Avg Customer Value, Campaign Response Rate, Complaint Rate.
Gráfico de línea: altas de clientes por mes (`Dt_Customer`) — tendencia de crecimiento.
Barras: ingreso total por Educación / Estado civil.

**Página 2 — Campañas** → *¿qué campaña funciona mejor y con qué cliente?*
Barras: tasa de aceptación por campaña (tabla `Campaign`).
Matriz: tasa de aceptación por `Age Group` / `Spend Tier` / `Has Children`.
Dispersión: `Income` vs `Total_Campaigns_Accepted`, color por `Education`.

**Página 3 — Canales** → *¿qué canal genera más ingresos y en qué segmento?*
Donut/barras: compras por canal (tabla `Channel`).
Barras apiladas: compras por canal, desglosado por `Age Group` o `Has Children`.
Tarjetas: Web Conversion Proxy, media de `NumWebVisitsMonth`.

**Página 4 — Oportunidades de crecimiento** → *upsell, cross-sell, retención*
Matriz: `Spend Tier` × `Campaign Response Rate` — clientes de alto gasto que no responden a campañas = oportunidad de upsell.
Dispersión: `Recency` vs `Total_Spend` — clientes valiosos con alta recencia (mucho tiempo sin comprar) = riesgo de churn, prioridad de retención.
Barras: gasto por categoría de producto (tabla `Category`), desglosado por `Spend Tier` — qué categoría cross-sellear a cada segmento.

## 6. Filtros/slicers recomendados

`Education`, `Marital_Status`, `Has Children`, `Age Group`, `Spend Tier`, rango de fechas de `Dt_Customer`.

## 7. Siguiente paso

Con las páginas 2-4 ya tienes contenido suficiente para extraer 3-4 insights concretos (con su "so what") que alimentarán el dashboard HTML final.
