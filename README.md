# ENU Guardian — Zero SLA Breaches

Prototipo de agente autónomo que monitorea temporizadores ENU en casos de soporte Wiser (simulados) e interviene antes de que el cliente note un incumplimiento de SLA.

**Demo loop:** `MONITOR → TRIGGER → ANALYZE → NOTIFY`. En el paso NOTIFY, si hay una API key de DeepSeek configurada, el borrador de la actualización al cliente se genera en vivo con `deepseek-chat`; si no, usa plantillas integradas.

## Cómo funciona

- App 100% estática: un solo `index.html` (Preact + HTM desde CDN). **No hay backend ni build.**
- Los casos son datos simulados incluidos en el código.
- La API key de DeepSeek se guarda solo en `localStorage` del navegador y se envía directo a `api.deepseek.com`.

## Ejecutar localmente

```bash
# opción 1
python3 -m http.server 8080
# opción 2
npx serve
```

Abrir http://localhost:8080

## Conectar DeepSeek

1. Clic en el botón **"DeepSeek: Off"** en el header.
2. Pegar tu API key (`sk-...`) de https://platform.deepseek.com
3. **Save** (y opcionalmente **Test connection**).
4. El botón cambia a **"DeepSeek: Live"** y el paso NOTIFY llama a DeepSeek en vivo.

> ⚠️ Al no haber backend, la key vive en el navegador de quien la pega. Para demos públicas usa una key desechable con poco crédito y revócala después.

## Desplegar gratis

### Vercel (recomendado)

1. Entra a https://vercel.com y haz login con GitHub.
2. **Add New → Project → Import** `carbler/ENU-Guardian`.
3. Framework Preset: **Other**. Sin build command, sin output directory (raíz).
4. **Deploy**. Listo — URL tipo `enu-guardian.vercel.app`.

### GitHub Pages (alternativa, también gratis)

1. En el repo: **Settings → Pages**.
2. Source: **Deploy from a branch** → rama `main`, carpeta `/ (root)`.
3. **Save**. En ~1 min queda en `https://carbler.github.io/ENU-Guardian/`.
