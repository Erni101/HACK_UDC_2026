# HACK_UDC_2026
Repositorio para trabajar en equipo [Vigues,Lolo,Lucas,Ernesto]

## Ejecutar con Docker (Grafana + Backend)

1. Configura tu API key de TomTom (elige una opción):

```bash
export TOMTOM_API_KEY="TU_API_KEY"
```

o creando `Docker_grafana/.env` a partir de `Docker_grafana/.env.example`.

2. Levanta los contenedores desde `Docker_grafana/`:

```bash
docker compose up --build -d
```

3. Abre Grafana en `http://localhost:3000`.

## Importante: `localhost` en Grafana

Dentro de Grafana, si configuras un datasource HTTP, **no uses `localhost:5000`** para el backend.

Usa la URL interna de Docker:

`http://backend_python:5000/api/accidentes`

`localhost` dentro de Grafana apunta al propio contenedor de Grafana, no a tu backend.
