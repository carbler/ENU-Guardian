// Vercel serverless proxy for DeepSeek. The API key lives in the
// DEEPSEEK_API_KEY environment variable and never reaches the browser.
export default async function handler(req, res) {
  const apiKey = process.env.DEEPSEEK_API_KEY || process.env.DEEP_SEEK_API_KEY;

  if (req.method === 'GET') {
    return res.status(200).json({ configured: !!apiKey });
  }
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }
  if (!apiKey) {
    return res.status(503).json({ error: 'DEEPSEEK_API_KEY not configured' });
  }

  const { system, user } = req.body || {};
  if (typeof system !== 'string' || typeof user !== 'string' || system.length > 4000 || user.length > 8000) {
    return res.status(400).json({ error: 'Invalid payload' });
  }

  try {
    const r = await fetch('https://api.deepseek.com/chat/completions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${apiKey}` },
      body: JSON.stringify({
        model: 'deepseek-chat',
        temperature: 0.7,
        max_tokens: 300,
        messages: [
          { role: 'system', content: system },
          { role: 'user', content: user }
        ]
      })
    });
    if (!r.ok) {
      let detail = `HTTP ${r.status}`;
      try { const j = await r.json(); if (j?.error?.message) detail = j.error.message; } catch (e) { /* keep HTTP status */ }
      return res.status(502).json({ error: detail });
    }
    const data = await r.json();
    const text = data?.choices?.[0]?.message?.content?.trim();
    if (!text) return res.status(502).json({ error: 'empty completion' });
    return res.status(200).json({ text });
  } catch (err) {
    return res.status(502).json({ error: err.message || 'DeepSeek request failed' });
  }
}
