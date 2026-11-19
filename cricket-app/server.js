const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const { Pool } = require('pg');
const path = require('path');

const app = express();
const server = http.createServer(app);
const io = new Server(server);

app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

const ADMIN_PASSWORD = process.env.ADMIN_PASSWORD || 'admin123';

const pool = new Pool({
  host: process.env.DB_HOST || 'cricket-db',
  port: process.env.DB_PORT || 5432,
  user: process.env.POSTGRESQL_USER || 'cricket',
  password: process.env.POSTGRESQL_PASSWORD || 'cricketpass',
  database: process.env.POSTGRESQL_DATABASE || 'cricketdb',
});

async function initDB() {
  await pool.query(`
    CREATE TABLE IF NOT EXISTS match_info (
      id INT PRIMARY KEY DEFAULT 1,
      team_a VARCHAR(50) DEFAULT 'INDIA',
      team_b VARCHAR(50) DEFAULT 'AUSTRALIA',
      batting_team VARCHAR(50) DEFAULT 'INDIA',
      overs_limit INT DEFAULT 20,
      striker VARCHAR(50) DEFAULT 'V. Kohli',
      non_striker VARCHAR(50) DEFAULT 'R. Sharma',
      bowler VARCHAR(50) DEFAULT 'M. Starc',
      status VARCHAR(30) DEFAULT 'LIVE - 1ST INNINGS'
    );
  `);

  await pool.query(`
    CREATE TABLE IF NOT EXISTS ball_events (
      id SERIAL PRIMARY KEY,
      runs INT NOT NULL DEFAULT 0,
      extra_type VARCHAR(15) NOT NULL DEFAULT 'NONE',
      is_wicket BOOLEAN NOT NULL DEFAULT FALSE,
      label VARCHAR(10) NOT NULL,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
  `);

  await pool.query(`
    INSERT INTO match_info (id) VALUES (1) ON CONFLICT (id) DO NOTHING;
  `);
}

async function getScoreState() {
  const matchRes = await pool.query('SELECT * FROM match_info WHERE id = 1');
  const ballsRes = await pool.query('SELECT * FROM ball_events ORDER BY id ASC');

  const match = matchRes.rows[0];
  const events = ballsRes.rows;

  let totalRuns = 0;
  let wickets = 0;
  let legalBalls = 0;

  for (const ev of events) {
    totalRuns += ev.runs;
    if (ev.is_wicket) wickets += 1;
    if (ev.extra_type === 'NONE' || ev.extra_type === 'BYE') {
      legalBalls += 1;
    }
  }

  const completedOvers = Math.floor(legalBalls / 6);
  const ballsInCurrentOver = legalBalls % 6;
  const oversDisplay = `${completedOvers}.${ballsInCurrentOver}`;
  const crr = legalBalls > 0 ? ((totalRuns / legalBalls) * 6).toFixed(2) : '0.00';

  // Last 12 balls for timeline
  const timeline = events.slice(-12).map(e => ({
    id: e.id,
    label: e.label,
    isWicket: e.is_wicket,
    runs: e.runs,
    extra: e.extra_type
  }));

  return {
    match,
    score: {
      runs: totalRuns,
      wickets,
      overs: oversDisplay,
      legalBalls,
      crr
    },
    timeline
  };
}

// Middleware to check admin password
function checkAuth(req, res, next) {
  const token = req.headers['x-admin-password'];
  if (token !== ADMIN_PASSWORD) {
    return res.status(401).json({ error: 'Invalid Admin Password' });
  }
  next();
}

// Get full live state
app.get('/api/state', async (req, res) => {
  try {
    const state = await getScoreState();
    res.json(state);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Update match teams / players / status
app.post('/api/match', checkAuth, async (req, res) => {
  const { team_a, team_b, batting_team, overs_limit, striker, non_striker, bowler, status } = req.body;
  try {
    await pool.query(
      `UPDATE match_info SET 
        team_a = COALESCE($1, team_a),
        team_b = COALESCE($2, team_b),
        batting_team = COALESCE($3, batting_team),
        overs_limit = COALESCE($4, overs_limit),
        striker = COALESCE($5, striker),
        non_striker = COALESCE($6, non_striker),
        bowler = COALESCE($7, bowler),
        status = COALESCE($8, status)
       WHERE id = 1`,
      [team_a, team_b, batting_team, overs_limit, striker, non_striker, bowler, status]
    );
    const state = await getScoreState();
    io.emit('scoreUpdate', state);
    res.json(state);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Record a ball event
app.post('/api/ball', checkAuth, async (req, res) => {
  const { runs = 0, extra_type = 'NONE', is_wicket = false } = req.body;

  let label = `${runs}`;
  if (is_wicket) label = runs > 0 ? `W+${runs}` : 'W';
  else if (extra_type === 'WIDE') label = runs > 1 ? `Wd+${runs - 1}` : 'Wd';
  else if (extra_type === 'NOBALL') label = runs > 1 ? `NB+${runs - 1}` : 'NB';
  else if (extra_type === 'BYE') label = `B${runs}`;

  try {
    await pool.query(
      'INSERT INTO ball_events (runs, extra_type, is_wicket, label) VALUES ($1, $2, $3, $4)',
      [runs, extra_type, is_wicket, label]
    );
    const state = await getScoreState();
    io.emit('scoreUpdate', state);
    res.json(state);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Undo last ball
app.post('/api/undo', checkAuth, async (req, res) => {
  try {
    await pool.query(
      'DELETE FROM ball_events WHERE id = (SELECT MAX(id) FROM ball_events)'
    );
    const state = await getScoreState();
    io.emit('scoreUpdate', state);
    res.json(state);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Reset entire match score
app.post('/api/reset', checkAuth, async (req, res) => {
  try {
    await pool.query('TRUNCATE TABLE ball_events RESTART IDENTITY');
    const state = await getScoreState();
    io.emit('scoreUpdate', state);
    res.json(state);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

const PORT = process.env.PORT || 8080;
initDB()
  .then(() => {
    server.listen(PORT, () => console.log(`Cricket server running on port ${PORT}`));
  })
  .catch(err => {
    console.error('Database initialization failed:', err);
    process.exit(1);
  });
