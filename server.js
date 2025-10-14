const express = require('express');
const fs = require('fs');

const app = express();
const PORT = 3000;

app.use(express.urlencoded({ extended: true }));
app.use(express.static(__dirname));

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
      return res.send('Login failed: Invalid credentials.');
    }

    const users = data.split('\n');
    const isValidUser = users.some(line => {
      if (!line) return false;
      // users.txt will be saved as [username, email, password]
      const parts = line.split(':');
      // Check if username (parts[0]) and password (parts[2]) match
      return parts[0] === username && parts[2] === password;
    });

    if (isValidUser) {
      // If login is successful, send back the script
      res.send(`
        <script>
          sessionStorage.setItem('loggedInUser', '${username}');
          window.location.href = '/';
        </script>
      `);
    } else {
      res.send('<h1>Login Failed</h1><p>Incorrect username or password.</p><a href="/login%20page.html">Try Again</a>');
    }
  });
});

// --- Start Server ---
app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});