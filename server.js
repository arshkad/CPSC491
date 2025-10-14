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
      // If the file can't be read, redirect with an error
      return res.redirect('/login%20page.html?error=1');
    }

    const users = data.split('\n');
    const isValidUser = users.some(line => {
      if (!line) return false;
      const parts = line.split(':');
      return parts[0] === username && parts[2] && parts[2].trim() === password;
    });

    if (isValidUser) {
      // On success, go to the home page
      res.send(`
        <script>
          sessionStorage.setItem('loggedInUser', '${username}');
          window.location.href = '/home.html';
        </script>
      `);
    } else {
      // On failure, redirect back to the login page with an error flag
      res.redirect('/login%20page.html?error=1');
    }
  });
});

// --- Start Server ---
app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});