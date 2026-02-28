# src/ — Código fuente

Este directorio contiene el código fuente principal del proyecto.

## 📂 Organización sugerida

```
src/
├── main.py          # Punto de entrada principal
├── config.py        # Configuración global (rutas, parámetros…)
├── data/
│   ├── loader.py    # Carga y validación de datos
│   └── preprocess.py# Limpieza y transformación
├── models/
│   └── model.py     # Lógica del modelo / algoritmo principal
├── utils/
│   └── helpers.py   # Funciones auxiliares reutilizables
└── api/             # (Opcional) Servidor / endpoints
    └── app.py
```

> Adapta esta estructura al reto elegido. Crea subcarpetas según sea necesario.

## ▶️ Ejecutar

```bash
python src/main.py
```

## 📝 Notas

- Mantén cada módulo con una responsabilidad única.
- Documenta las funciones públicas con docstrings.
- Importa siempre desde la raíz del proyecto para evitar problemas de paths:
  ```python
  from src.data.loader import load_dataset
  ```
