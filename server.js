// server.js
import express from 'express';
import fetch from 'node-fetch';
import bodyParser from 'body-parser';

const app = express();
app.use(bodyParser.json());

// Simulated database
let reportsDB = [];

// Helper function: reverse geocode
async function reverseGeocode(lat, lon) {
  try {
    const res = await fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}`);
    const data = await res.json();
    return data.display_name || `${lat}, ${lon}`;
  } catch (err) {
    console.error('Reverse geocode error:', err);
    return `${lat}, ${lon}`;
  }
}

// Endpoint to save report
app.post('/api/report-location', async (req, res) => {
  const { latitude, longitude, description } = req.body;
  const locationName = await reverseGeocode(latitude, longitude);

  const report = {
    Id: reportsDB.length + 1,
    Name: 'Anonymous', // you can customize
    Latitude: latitude,
    Longitude: longitude,
    Location: locationName,
    Type: 'Unknown',
    Description: description || '',
    'Urgency Level': 'Unknown',
    Timestamp: new Date().toISOString()
  };

  reportsDB.push(report);

  res.json({ success: true, report });
});

// Endpoint to get reports (with optional urgency filter)
app.get('/api/reports', (req, res) => {
  const urgencyFilter = req.query.urgency;
  let reports = reportsDB;

  if (urgencyFilter) {
    reports = reports.filter(r => r['Urgency Level'] === urgencyFilter);
  }

  res.json(reports);
});

app.listen(3000, () => console.log('Server running on http://localhost:3000'));
