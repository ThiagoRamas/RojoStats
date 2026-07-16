# 🔴 RojoStats

Aplicación desarrollada en Python para consultar estadísticas públicas del canal oficial de YouTube del Club Atlético Independiente y actualizar automáticamente un mensaje en Telegram.

> RojoStats es un proyecto independiente y no oficial. No está afiliado, patrocinado ni administrado por el Club Atlético Independiente.

---

## 📌 Descripción

RojoStats obtiene información pública mediante la YouTube Data API v3 y muestra en Telegram:

- Cantidad de suscriptores.
- Visualizaciones totales.
- Cantidad de videos publicados.
- Variación respecto de la medición anterior.
- Fecha y hora de la última actualización.

El bot publica un único mensaje y lo edita en cada actualización, evitando enviar mensajes repetidos al canal.

---

## 📸 Vista previa

El mensaje publicado en Telegram incluye un panel similar al siguiente:

```text
🔴 ROJOSTATS
Estadísticas digitales de Independiente

━━━━━━━━━━━━━━━━━━━━

📺 YouTube
Club Atlético Independiente

👥 Suscriptores
112.000
Variación: +1.000

👁️ Visualizaciones totales
13.122.992
Variación: +25.000

🎬 Videos publicados
1.119
Variación: +1

━━━━━━━━━━━━━━━━━━━━

🕒 Última actualización
16/07/2026 - 11:00git clone https://github.com/ThiagoRamas/RojoStats.git
cd RojoStats