# data/ — Datasets

Este directorio almacena los datos utilizados en el proyecto.

## 📂 Organización sugerida

```
data/
├── raw/         # Datos originales sin modificar (no tocar)
├── processed/   # Datos limpios y listos para usar
└── external/    # Datos de fuentes externas
```

## ⚠️ Reglas importantes

- **No versiones archivos grandes** (>5 MB). El `.gitignore` ya excluye `.csv`, `.json`, `.xlsx`, `.zip` y `.tar.gz`.
- Si necesitas compartir un dataset con el equipo, súbelo a Google Drive / Dropbox y añade el enlace aquí.

## 🔗 Fuentes de datos

| Dataset | Descripción | Enlace | Formato |
|---------|-------------|--------|---------|
| *(TBD)* | *(TBD)*     | *(TBD)*| *(TBD)* |

## 📥 Cómo descargar los datos

```bash
# Ejemplo con wget:
# wget -P data/raw/ <URL_DEL_DATASET>
```
