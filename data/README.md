# Datos

Este proyecto usa el dataset **Customer Personality Analysis** de Kaggle:
https://www.kaggle.com/datasets/rodsaldanha/arketing-campaign

El CSV no se versiona en este repositorio (requiere una cuenta de Kaggle para descargarlo). Para obtenerlo:

## Opción 1: descarga manual

1. Entra en el [enlace del dataset](https://www.kaggle.com/datasets/rodsaldanha/arketing-campaign) (necesitas cuenta de Kaggle).
2. Descarga el archivo y descomprímelo.
3. Coloca el CSV resultante en `data/raw/marketing_campaign.csv`.

## Opción 2: Kaggle API

```bash
pip install kaggle
# Coloca tu kaggle.json (API token) en ~/.kaggle/kaggle.json
kaggle datasets download -d rodsaldanha/arketing-campaign -p data/raw --unzip
```

## Estructura

```
data/raw/         # Dataset original, sin modificar (ignorado por git)
data/processed/   # Dataset limpio, listo para Power BI / dashboard (se añadirá en la siguiente fase)
```
