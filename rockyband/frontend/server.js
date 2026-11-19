const express = require('express');
const os = require('os');
const path = require('path');

const app = express();
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

const BACKEND_URL = process.env.BACKEND_URL || 'http://rocky-backend:8080';
const BAND_NAME = process.env.BAND_NAME || 'ROCKY BAND';
const TOUR_TITLE = process.env.TOUR_TITLE || 'WORLD TOUR 2026';

// Expose ConfigMap banner + which Frontend Pod served this request
app.get('/ui-info', (req, res) => {
  res.json({
    bandName: BAND_NAME,
    tourTitle: TOUR_TITLE,
    frontendPod: os.hostname(),
    backendTarget: BACKEND_URL
  });
});

// Proxy GET /api/tour -> rocky-backend Service
app.get('/api/tour', async (req, res) => {
  try {
    const response = await fetch(`${BACKEND_URL}/api/tour`);
    const data = await response.json();
    if (!response.ok) {
      return res.status(response.status).json({ ...data, frontendPod: os.hostname() });
    }
    res.json({ ...data, frontendPod: os.hostname() });
  } catch (err) {
    console.error('Frontend -> Backend connection failed:', err.message);
    res.status(502).json({
      error: `Cannot reach backend service (${BACKEND_URL}): ${err.message}`,
      frontendPod: os.hostname()
    });
  }
});

// Proxy POST /api/shoutouts -> rocky-backend Service
app.post('/api/shoutouts', async (req, res) => {
  try {
    const response = await fetch(`${BACKEND_URL}/api/shoutouts`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(req.body)
    });
    const data = await response.json();
    if (!response.ok) {
      return res.status(response.status).json({ ...data, frontendPod: os.hostname() });
    }
    res.json({ ...data, frontendPod: os.hostname() });
  } catch (err) {
    res.status(502).json({
      error: `Cannot reach backend service (${BACKEND_URL}): ${err.message}`,
      frontendPod: os.hostname()
    });
  }
});

const PORT = process.env.PORT || 8080;
app.listen(PORT, () => console.log(`RockyBand Frontend [${os.hostname()}] running on port ${PORT}`));
