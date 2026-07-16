# ENU Guardian — Zero SLA Breaches

Prototipo de agente autónomo que monitorea temporizadores ENU en casos de soporte Wiser (simulados) e interviene antes de que el cliente note un incumplimiento de SLA.

**Demo loop:** `MONITOR → TRIGGER → ANALYZE → NOTIFY`. Cuando un caso cruza el umbral, el agente lo analiza, redacta una actualización para el cliente a partir del estado del caso y la publica en el activity stream, reiniciando el temporizador.

## Cómo funciona

- App 100% estática: un solo `index.html` (Preact + HTM desde CDN). Sin backend, sin build, sin API keys.
- Los casos y las actualizaciones son datos simulados incluidos en el código.

## Ejecutar localmente

```bash
python3 -m http.server 8080
```

Abrir http://localhost:8080

## Desplegar gratis

### Vercel

1. Entra a https://vercel.com y haz login con GitHub.
2. **Add New → Project → Import** `carbler/ENU-Guardian`.
3. Framework Preset: **Other**. Sin build command, sin output directory (raíz).
4. **Deploy**. Listo — URL tipo `enu-guardian.vercel.app`.

### GitHub Pages (también gratis)

1. En el repo: **Settings → Pages**.
2. Source: **Deploy from a branch** → rama `main`, carpeta `/ (root)`.
3. **Save**. En ~1 min queda en `https://carbler.github.io/ENU-Guardian/`.
