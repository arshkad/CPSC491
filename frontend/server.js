const express = require('express');
const fs = require('fs');
const axios = require('axios');

const app = express();
const PORT = 3000;

app.use(express.urlencoded({ extended: true }));
app.use(express.static(__dirname));
app.use(express.json());

// Handle POST request for new user signup
app.post('/signup', (req, res) => {
  const { username, password, email } = req.body;
  const userRecord = `${username}:${email}:${password}\n`;

  fs.appendFile('users.txt', userRecord, (err) => {
    if (err) {
      console.error("Failed to save user:", err);
      return res.send('Error creating account.');
    }
    console.log(`New user registered: ${username}`);
    res.redirect('/login%20page.html');
  });
});

// Handle POST request for user login
app.post('/login', (req, res) => {
  const { username, password } = req.body;

  fs.readFile('users.txt', 'utf8', (err, data) => {
    if (err) {
      return res.redirect('/login%20page.html?error=1');
    }

    const users = data.split(/\r?\n/);
    const isValidUser = users.some(line => {
      if (!line) return false;
      const parts = line.split(':');
      return parts[0] === username && parts[2] && parts[2].trim() === password;
    });

    if (isValidUser) {
      res.send(`
        <script>
          sessionStorage.setItem('loggedInUser', '${username}');
          window.location.href = '/Dashboard.html';
        </script>
      `);
    } else {
      res.redirect('/login%20page.html?error=1');
    }
  });
});

app.post('/analyze', async (req, res) => {
  try {
    // Gets JSON data through index.html
    const colorData = req.body;
    console.log('Got color data from browser:', colorData);

    // Puts JSON into Python server
    const pythonResponse = await axios.post(
      'http://localhost:5001/analyze',
      colorData,
      {
        headers: { 'Content-Type': 'application/json' }
      }
    );

    // Sends AI response back to browser
    console.log('Got response from Python:', pythonResponse.data);
    res.json(pythonResponse.data);

  } catch (error) {
    console.error("Error in /analyze (JSON) route:", error.message);
    res.status(500).json({ error: 'Failed to analyzze colors' });
  }
});

// --- Start Server ---
app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});