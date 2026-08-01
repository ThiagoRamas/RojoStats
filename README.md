# 🔴 RojoStats

> Monitor automatizado de analítica pública de YouTube para el Club Atlético Independiente.

![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![YouTube Data API](https://img.shields.io/badge/YouTube_Data_API-v3-FF0000?style=flat-square&logo=youtube&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram-Bot_API-26A5E4?style=flat-square&logo=telegram&logoColor=white)
![GitHub Actions](https://img.shields.io/github/actions/workflow/status/ThiagoRamas/RojoStats/actualizar.yml?style=flat-square&logo=githubactions&label=hourly%20update)
![Tests](https://img.shields.io/badge/tests-10%20passing-success?style=flat-square)

## Descripción

RojoStats transforma estadísticas públicas del canal oficial de YouTube de Independiente en un informe de crecimiento actualizado automáticamente. El sistema consulta la API oficial, conserva una serie histórica, calcula comparaciones temporales, analiza el rendimiento de videos recientes y actualiza un único mensaje de Telegram sin generar spam.

El proyecto está pensado como una solución pequeña pero completa de integración, automatización y análisis de datos.

## Funcionalidades

- Consulta de suscriptores, visualizaciones y videos publicados.
- Comparaciones contra el inicio del día, 7 días y 30 días.
- Porcentajes de crecimiento y promedios diarios.
- Historial horario durante 7 días y resumen diario para el largo plazo.
- Último video publicado con vistas, likes y comentarios.
- Video más visto de los últimos 30 días.
- Señales de aceleración, desaceleración y nuevas publicaciones.
- Actualización del mismo mensaje de Telegram.
- Ejecución automática cada hora mediante GitHub Actions.
- Persistencia del historial entre ejecuciones.
- Pruebas automatizadas para historial, tendencias y respuestas de YouTube.

## Arquitectura

```text
YouTube Data API
        │
        ▼
youtube_service     Recolección y normalización
        │
        ▼
storage             Historial y compactación
        │
        ▼
analytics           Comparaciones, promedios y señales
        │
        ▼
telegram_service    Construcción y publicación del informe
        │
        ▼
GitHub Actions      Ejecución horaria y persistencia
```

### Estructura principal

```text
RojoStats/
├── .github/workflows/   # Automatización horaria
├── analytics/           # Señales y tendencias
├── storage/             # Estado e historial
├── telegram_service/    # Cliente y formato del informe
├── tests/               # Pruebas automatizadas
├── utils/               # Formateo numérico
├── youtube_service/     # Integración con YouTube
├── config.py
└── main.py
```

## Estrategia de historial

Cada ejecución registra una medición con horario argentino. Para mantener precisión sin hacer crecer el repositorio indefinidamente, RojoStats conserva todas las mediciones horarias de los últimos 7 días y una medición diaria para períodos anteriores.

Esto permite calcular tendencias semanales y mensuales utilizando referencias reales en lugar de comparar únicamente contra la ejecución anterior.

## Automatización

El workflow `.github/workflows/actualizar.yml` se ejecuta cada hora y también puede iniciarse manualmente. La automatización:

1. instala las dependencias;
2. consulta YouTube;
3. actualiza Telegram;
4. registra y compacta el historial;
5. persiste la nueva medición en el repositorio.

Las credenciales se almacenan como GitHub Actions Secrets y nunca se incluyen en el código.

## Instalación local

```powershell
git clone https://github.com/ThiagoRamas/RojoStats.git
cd RojoStats
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Crear un archivo `.env`:

```env
TOKEN=telegram_bot_token
CANAL=@canal_de_telegram
YOUTUBE_API_KEY=youtube_api_key
YOUTUBE_HANDLE=@Independiente
```

Ejecutar:

```powershell
python main.py
```

## Pruebas

```powershell
python -m unittest discover -s tests -v
```

La suite cubre cálculos diarios, semanales y mensuales, porcentajes, compactación, zonas horarias, señales de tendencia, métricas opcionales y sanitización de errores.

## Seguridad y alcance

- Las claves se gestionan mediante `.env` y GitHub Actions Secrets.
- Los mensajes de error no exponen credenciales.
- Solo se utilizan datos públicos obtenidos mediante APIs oficiales.
- No se utiliza scraping ni acceso no autorizado.
- El proyecto no está afiliado ni representa oficialmente al Club Atlético Independiente.

## Autor

**Thiago Ramas** — estudiante de Licenciatura en Sistemas.

Proyecto desarrollado con fines educativos y de portfolio.
