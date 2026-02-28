# HACK_UDC_2026

> Repositorio del equipo **[Vigues, Lolo, Lucas, Ernesto]** para el **Hackathon UDC 2026**.

---

## 📁 Estructura del proyecto

```
HACK_UDC_2026/
├── src/                    # Código fuente principal (paquete Python)
│   ├── __init__.py
│   ├── main.py             # Punto de entrada — ejecuta el pipeline completo
│   ├── config.py           # Configuración global (lee variables de .env)
│   ├── data/
│   │   └── loader.py       # Carga y división de datasets
│   ├── models/             # Lógica del modelo / algoritmo
│   ├── utils/
│   │   └── helpers.py      # Funciones auxiliares (timer, logging, flatten…)
│   └── api/                # Servidor / endpoints (opcional)
├── docs/
│   ├── arquitectura.md     # Diagrama y decisiones técnicas
│   └── ideas.md            # Brainstorming y plan de trabajo
├── data/
│   ├── raw/                # Datos originales sin modificar
│   ├── processed/          # Datos limpios listos para usar
│   └── external/           # Datos de fuentes externas
├── notebooks/
│   └── 01_exploracion_datos.ipynb  # Exploración inicial del dataset
├── tests/
│   ├── conftest.py         # Fixtures compartidas de pytest
│   ├── test_helpers.py     # Tests de src/utils/helpers.py
│   ├── test_loader.py      # Tests de src/data/loader.py
│   └── test_config.py      # Tests de src/config.py
├── .env.example            # Plantilla de variables de entorno
├── .gitignore
├── CONTRIBUTING.md         # Guía de contribución y convención de commits
├── Makefile                # Comandos de uso frecuente
├── pyproject.toml          # Configuración del paquete Python
├── requirements.txt        # Dependencias con versiones mínimas
└── README.md
```

---

## 🚀 Cómo empezar

### Opción A — Makefile (recomendado)

```bash
git clone https://github.com/Erni101/HACK_UDC_2026.git
cd HACK_UDC_2026
make setup      # crea venv, instala deps, copia .env.example → .env
source venv/bin/activate
```

### Opción B — Manual

```bash
git clone https://github.com/Erni101/HACK_UDC_2026.git
cd HACK_UDC_2026
python -m venv venv
source venv/bin/activate   # Linux / macOS
# venv\Scripts\activate    # Windows
pip install -r requirements.txt
pip install -e .           # instala src/ como paquete editable
cp .env.example .env       # edita .env con tus valores
```

### Comandos útiles

| Comando         | Descripción                              |
|-----------------|------------------------------------------|
| `make setup`    | Crea el entorno e instala dependencias   |
| `make run`      | Ejecuta el pipeline principal            |
| `make test`     | Lanza los tests con pytest               |
| `make test-cov` | Tests + informe de cobertura             |
| `make lint`     | Comprueba el estilo del código (ruff)    |
| `make notebook` | Abre JupyterLab                          |
| `make clean`    | Elimina cachés y artefactos              |
| `make help`     | Muestra todos los comandos disponibles   |

### Crear una rama para tu trabajo

```bash
git checkout -b feature/nombre-funcionalidad
```

Consulta [CONTRIBUTING.md](CONTRIBUTING.md) para la convención de commits y el flujo de trabajo del equipo.

---

## 👥 Equipo

| Miembro   | GitHub |
|-----------|--------|
| Ernesto   | [@Erni101](https://github.com/Erni101) |
| Vigues    |        |
| Lolo      |        |
| Lucas     |        |

---

## 📝 Descripción del problema

> *A completar una vez se conozca el reto de la empresa.*

Consulta [docs/ideas.md](docs/ideas.md) para el brainstorming del equipo.

---

## 🏗️ Arquitectura

> *A completar una vez se defina la solución técnica.*

Consulta [docs/arquitectura.md](docs/arquitectura.md) para el diagrama y descripción de la arquitectura.

---

## 🛠️ Tecnologías (tentativas)

- Python 3.9+
- pandas, scikit-learn, matplotlib / seaborn
- Jupyter Notebooks
- pytest + ruff
- Git / GitHub

---

## 📄 Licencia

[MIT](LICENSE)
