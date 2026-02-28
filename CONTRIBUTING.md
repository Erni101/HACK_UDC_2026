# Guía de Contribución — HACK_UDC_2026

Gracias por contribuir al proyecto. Sigue estas pautas para mantener el código ordenado y trabajar bien en equipo durante el hackathon.

---

## 🌿 Flujo de trabajo con Git

Usamos el modelo **Feature Branch Workflow**:

```
main
 └── feature/<nombre>      # Nueva funcionalidad
 └── fix/<nombre>          # Corrección de bug
 └── docs/<nombre>         # Documentación
 └── refactor/<nombre>     # Refactorización
```

### Pasos

1. Sincroniza tu rama local con `main`:
   ```bash
   git checkout main
   git pull origin main
   ```

2. Crea tu rama:
   ```bash
   git checkout -b feature/mi-funcionalidad
   ```

3. Haz tus cambios y commitea siguiendo la convención de abajo.

4. Sube tu rama y abre un Pull Request:
   ```bash
   git push origin feature/mi-funcionalidad
   ```

5. Solicita revisión a al menos un compañero antes de mergear.

---

## ✍️ Convención de commits

Usamos [Conventional Commits](https://www.conventionalcommits.org/):

```
<tipo>: <descripción corta en imperativo>
```

| Tipo       | Cuándo usarlo |
|------------|---------------|
| `feat`     | Nueva funcionalidad |
| `fix`      | Corrección de bug |
| `docs`     | Cambios en documentación |
| `refactor` | Refactorización sin cambio de comportamiento |
| `test`     | Añadir o modificar tests |
| `chore`    | Tareas de mantenimiento (deps, configuración…) |
| `data`     | Cambios en datos o datasets |

**Ejemplos:**

```
feat: añadir endpoint de predicción
fix: corregir carga de CSV con encoding UTF-8
docs: actualizar arquitectura con diagrama
test: añadir tests unitarios para el módulo de limpieza
```

---

## 🗂️ Estructura de carpetas

| Carpeta      | Contenido |
|--------------|-----------|
| `src/`       | Código fuente Python (módulos, scripts, API…) |
| `notebooks/` | Exploración de datos y prototipos en Jupyter |
| `data/`      | Datasets crudos y procesados (no versionar archivos grandes) |
| `docs/`      | Documentación técnica y de producto |
| `tests/`     | Tests automáticos con pytest |

---

## ✅ Buenas prácticas

- Trabaja siempre en una rama, **nunca hagas commits directamente en `main`**.
- Mantén los commits pequeños y atómicos (un cambio = un commit).
- Ejecuta los tests antes de abrir un PR: `pytest tests/`
- Si cambias dependencias, actualiza `requirements.txt`.
- Los archivos de datos grandes (>5 MB) **no deben versionarse**; usa un enlace de Drive/Dropbox/etc. y documenta su ubicación en `data/README.md`.
