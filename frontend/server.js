const axios = require('axios');
const multer = require('multer');
const upload = multer({ storage: multer.memoryStorage() });

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

app.post('/analyze', upload.single('imageFile'), async (req, res) => {
  try {
    // Takes image from browser
    const image = req.file.buffer;

    // Sends image to server
    const formData = new FormData();
    formData.append('image', new Blob([image]), req.file.originalname);

    const pythonResponse = await axios.post('http://localhost:5000/extract_colors', formData);

    res.json(pythonResponse.data);

  } catch (error) {
    console.error("Error in /analyze:", error);
    res.status(500).json({ error: 'Failed to analyze image' });
  }
})

// --- Start Server ---
app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});