# notebooks/ — Jupyter Notebooks

Este directorio contiene notebooks de exploración, análisis y prototipado.

## 📂 Convención de nombres

```
<número>_<autor>_<descripción>.ipynb
```

**Ejemplos:**
```
01_ernesto_exploracion_datos.ipynb
02_lolo_limpieza_outliers.ipynb
03_vigues_modelo_baseline.ipynb
```

## ▶️ Cómo ejecutar los notebooks

```bash
# Activa el entorno virtual primero
source venv/bin/activate

# Lanza Jupyter
jupyter notebook
# o
jupyter lab
```

## 📝 Notas

- Los notebooks son para **exploración y prototipado**, no para código de producción.
- Una vez que el código de un notebook esté estable, muévelo a `src/`.
- Reinicia el kernel y ejecuta todas las celdas de arriba a abajo antes de commitear (`Kernel > Restart & Run All`).
- No subas notebooks con outputs muy grandes; limpia los outputs antes de commitear.
