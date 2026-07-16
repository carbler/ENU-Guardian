# ENU Guardian — Zero SLA Breaches

Prototipo de agente autónomo que monitorea temporizadores ENU en casos de soporte Wiser (simulados) e interviene antes de que el cliente note un incumplimiento de SLA.

**Demo loop:** `MONITOR → TRIGGER → ANALYZE → NOTIFY`. En el paso NOTIFY, si hay una API key de DeepSeek configurada, el borrador de la actualización al cliente se genera en vivo con `deepseek-chat`; si no, usa plantillas integradas.

## Cómo funciona

- App estática: un solo `index.html` (Preact + HTM desde CDN), sin build.
- `api/draft.js`: función serverless de Vercel que hace de proxy hacia DeepSeek — la key vive en una variable de entorno y **nunca llega al navegador**.
- Los casos son datos simulados incluidos en el código.

## La API key de DeepSeek (en orden de preferencia)

1. **Vercel (recomendado):** en el proyecto de Vercel → *Settings → Environment Variables* → agrega `DEEP_SEEK_API_KEY` (o `DEEPSEEK_API_KEY`) y redeploy. El botón del header mostrará "DeepSeek: Live (server)". La key queda encriptada en Vercel, invisible para quien vea la demo.
2. **Respaldo (GitHub Pages / local):** botón "DeepSeek: Off" en el header → pegar la key → Save. Queda solo en el `localStorage` de ese navegador y las llamadas van directo a `api.deepseek.com`. Cualquiera con DevTools puede verla: usa una key desechable.
3. Sin key: la demo funciona igual con plantillas integradas.

> El `.env` local está en `.gitignore` — **nunca subas la key al repo**. Solo lo usa `vercel dev` en local; el deploy lee la variable configurada en el dashboard de Vercel.

## Ejecutar localmente

```bash
# opción 1
python3 -m http.server 8080
# opción 2
npx serve
```

Abrir http://localhost:8080

## Desplegar gratis

### Vercel (recomendado — soporta el proxy serverless)

1. Entra a https://vercel.com y haz login con GitHub.
2. **Add New → Project → Import** `carbler/ENU-Guardian`.
3. Framework Preset: **Other**. Sin build command, sin output directory (raíz).
4. En el paso de configuración (o después en *Settings → Environment Variables*): agrega `DEEP_SEEK_API_KEY` con tu key.
5. **Deploy**. Listo — URL tipo `enu-guardian.vercel.app` con DeepSeek en vivo.

### GitHub Pages (alternativa, solo estático)

1. En el repo: **Settings → Pages**.
2. Source: **Deploy from a branch** → rama `main`, carpeta `/ (root)`.
3. **Save**. En ~1 min queda en `https://carbler.github.io/ENU-Guardian/`.
4. Aquí no corre la función serverless: DeepSeek funciona pegando la key en el navegador (opción 2 de arriba) o queda en modo plantilla.
