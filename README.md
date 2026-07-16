# ENU Guardian — Zero SLA Breaches

Prototipo de agente autónomo que monitorea temporizadores ENU en casos de soporte Wiser (simulados) e interviene antes de que el cliente note un incumplimiento de SLA.

**Demo loop:** `MONITOR → TRIGGER → ANALYZE → NOTIFY`. En el paso NOTIFY, si hay una API key de DeepSeek configurada, el borrador de la actualización al cliente se genera en vivo con `deepseek-chat`; si no, usa plantillas integradas.

## Cómo funciona

- App estática: un solo `index.html` (Preact + HTM desde CDN), sin build.
- `api/draft.js`: función serverless de Vercel que hace de proxy hacia DeepSeek — la key vive en la variable de entorno `DEEP_SEEK_API_KEY` y **nunca llega al navegador**. No hay campo para pegar keys: siempre usa la del entorno.
- Los casos son datos simulados incluidos en el código. Si la llamada a DeepSeek falla, hay un borrador de emergencia para que la demo no se rompa.

> El `.env` local está en `.gitignore` — **nunca subas la key al repo**. El deploy lee la variable configurada en el dashboard de Vercel.

## Ejecutar localmente

```bash
python3 dev-server.py 8080
```

Abrir http://localhost:8080 — el servidor de desarrollo sirve la app e implementa `/api/draft` leyendo `DEEP_SEEK_API_KEY` del `.env` (copia `.env.example` a `.env` y pon tu key).

## Desplegar gratis

### Vercel (necesario para DeepSeek en vivo)

1. Entra a https://vercel.com y haz login con GitHub.
2. **Add New → Project → Import** `carbler/ENU-Guardian`.
3. Framework Preset: **Other**. Sin build command, sin output directory (raíz).
4. En el paso de configuración (o después en *Settings → Environment Variables*): agrega `DEEP_SEEK_API_KEY` con tu key.
5. **Deploy**. Listo — URL tipo `enu-guardian.vercel.app` con DeepSeek en vivo ("DeepSeek: Live" en el header).

> GitHub Pages no sirve para esta versión: no ejecuta funciones serverless, así que DeepSeek nunca conectaría. Usa Vercel.
