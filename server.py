import asyncio
import websockets

# Store connected clients
connected_clients = set()

async def handle_client(websocket, path):
    # Add the client to the connected clients set
    connected_clients.add(websocket)
    print(f"New client connected: {websocket.remote_address}")

    try:
        async for message in websocket:
            print(f"Received message: {message}")
            # Broadcast the message to all connected clients
            for client in connected_clients:
                if client != websocket:  # Don't send the message back to the sender
                    await client.send(message)
    except websockets.ConnectionClosed:
        print(f"Client disconnected: {websocket.remote_address}")
    finally:
        # Remove the client from the connected clients set
        connected_clients.remove(websocket)

async def main():
    # Start the WebSocket server
    async with websockets.serve(handle_client, "0.0.0.0", 8765):
        print("WebSocket chat server is running on ws://localhost:8765")
        await asyncio.Future()  # Keep the server running indefinitely

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server stopped.")
