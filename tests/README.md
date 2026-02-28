# tests/ — Tests automáticos

Este directorio contiene los tests automáticos del proyecto usando **pytest**.

## ▶️ Ejecutar los tests

```bash
# Desde la raíz del proyecto
pytest tests/ -v
```

## 📂 Organización sugerida

```
tests/
├── test_loader.py       # Tests del módulo de carga de datos
├── test_preprocess.py   # Tests de preprocesado
└── test_model.py        # Tests del modelo / lógica principal
```

## ✍️ Convención de nombres

- Los archivos de test deben empezar por `test_`.
- Las funciones de test deben empezar por `test_`.

**Ejemplo:**
```python
# tests/test_loader.py
def test_load_csv_returns_dataframe():
    from src.data.loader import load_dataset
    df = load_dataset("data/raw/sample.csv")
    assert df is not None
    assert len(df) > 0
```

## 📝 Notas

- Crea un test por cada función importante en `src/`.
- Usa datos de muestra pequeños en `tests/fixtures/` para los tests.
- Los tests deben ejecutarse en menos de 30 segundos.
