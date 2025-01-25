const express = require('express');
const http = require('http');
const WebSocket = require('ws');

const app = express();

// Keep Glitch alive by responding to HTTP requests
app.get('/', (req, res) => {
  res.send('WebSocket server is running!');
});

// Create an HTTP server
const server = http.createServer(app);

// Get the port from Glitch's environment or default to 3000
const PORT = process.env.PORT || 3000;

// Start the HTTP server
server.listen(PORT, () => {
  console.log(`HTTP server is running on port ${PORT}`);
});

// Create a WebSocket server on the same HTTP server
const wss = new WebSocket.Server({ server });

// Set to store connected clients
const connectedClients = new Set();

// Handle new WebSocket connections
wss.on('connection', (ws) => {
  connectedClients.add(ws);
  console.log('New client connected');

  ws.on('message', (message) => {
    console.log(`Received message: ${message}`);

    // Broadcast the raw message to all connected clients except the sender
    connectedClients.forEach((client) => {
      if (client !== ws && client.readyState === WebSocket.OPEN) {
        client.send(message); // Send the raw message as plain text
      }
    });
  });

  // Handle client disconnection
  ws.on('close', () => {
    connectedClients.delete(ws);
    console.log('Client disconnected');
  });

  // Handle errors
  ws.on('error', (error) => {
    console.error('WebSocket error:', error);
  });
});
