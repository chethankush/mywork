const express = require('express');
const { Pool } = require('pg');
const os = require('os');

const app = express();
app.use(express.json());

const pool = new Pool({
  host: process.env.DB_HOST || 'rocky-db',
  port: process.env.DB_PORT || 5432,
  user: process.env.POSTGRESQL_USER,
  password: process.env.POSTGRESQL_PASSWORD,
  database: process.env.POSTGRESQL_DATABASE,
});

async function initDB() {
  await pool.query(`
    CREATE TABLE IF NOT EXISTS concerts (
      id SERIAL PRIMARY KEY,
      city VARCHAR(60) NOT NULL,
      venue VARCHAR(100) NOT NULL,
      show_date VARCHAR(40) NOT NULL,
      tickets_status VARCHAR(30) DEFAULT 'AVAILABLE'
    );
  `);

  await pool.query(`
    CREATE TABLE IF NOT EXISTS shoutouts (
      id SERIAL PRIMARY KEY,
      fan_name VARCHAR(50) NOT NULL,
      message VARCHAR(200) NOT NULL,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
  `);

  const countRes = await pool.query('SELECT COUNT(*) FROM concerts');
  if (parseInt(countRes.rows[0].count, 10) === 0) {
    await pool.query(`
      INSERT INTO concerts (city, venue, show_date, tickets_status) VALUES
      ('BENGALURU', 'Palace Grounds Arena', 'DEC 12, 2026', 'SELLING FAST'),
      ('MUMBAI', 'Mahalaxmi Racecourse', 'DEC 19, 2026', 'AVAILABLE'),
      ('LONDON', 'Wembley Stadium', 'JAN 15, 2027', 'SOLD OUT'),
      ('TOKYO', 'Tokyo Dome', 'FEB 04, 2027', 'AVAILABLE');
    `);
  }
}

// Health check endpoint
app.get('/health', async (req, res) => {
  try {
    await pool.query('SELECT 1');
    res.json({ status: 'UP', backendPod: os.hostname(), db: 'CONNECTED' });
  } catch (err) {
    res.status(500).json({ status: 'DOWN', backendPod: os.hostname(), error: err.message });
  }
});

// Get tour dates + fan shoutouts
app.get('/api/tour', async (req, res) => {
  try {
    const concerts = await pool.query('SELECT * FROM concerts ORDER BY id ASC');
    const shoutouts = await pool.query('SELECT * FROM shoutouts ORDER BY id DESC LIMIT 10');
    res.json({
      backendPod: os.hostname(),
      concerts: concerts.rows,
      shoutouts: shoutouts.rows
    });
  } catch (err) {
    console.error('Database query error:', err.message);
    res.status(500).json({ error: 'Backend DB connection failed: ' + err.message, backendPod: os.hostname() });
  }
});

// Post a new fan shoutout
app.post('/api/shoutouts', async (req, res) => {
  const { fan_name, message } = req.body;
  if (!fan_name || !message) {
    return res.status(400).json({ error: 'Name and message are required' });
  }
  try {
    await pool.query('INSERT INTO shoutouts (fan_name, message) VALUES ($1, $2)', [fan_name, message]);
    res.json({ success: true, backendPod: os.hostname() });
  } catch (err) {
    console.error('Database insert error:', err.message);
    res.status(500).json({ error: 'Backend DB write failed: ' + err.message, backendPod: os.hostname() });
  }
});

const PORT = process.env.PORT || 8080;
initDB()
  .then(() => {
    app.listen(PORT, () => console.log(`RockyBand Backend [${os.hostname()}] listening on port ${PORT}`));
  })
  .catch(err => {
    console.error('FATAL: Could not connect to PostgreSQL on startup:', err.message);
    process.exit(1);
  });
