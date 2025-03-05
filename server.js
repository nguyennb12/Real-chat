const WebSocket = require('ws');

const PORT = process.env.PORT || 5000;
const server = new WebSocket.Server({ port: PORT });
console.log(`WebSocket server is running on ws://localhost:${PORT}`);

server.on('connection', (ws) => {
    console.log('New client connected');

    ws.on('message', (message) => {
        console.log(`Received: ${message}`);
        // Broadcast to all connected clients except the sender
        server.clients.forEach((client) => {
            if (client !== ws && client.readyState === WebSocket.OPEN) {
                client.send(message);
            }
        });
    });
    ws.on('close', () => {
        console.log('Client disconnected');
    });
});