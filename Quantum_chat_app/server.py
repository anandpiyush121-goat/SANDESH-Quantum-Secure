from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pymongo import MongoClient
import json
from datetime import datetime

app = FastAPI()

# --- MONGODB CONNECTION SETUP ---
# Standard localhost port for MongoDB is 27017
client = MongoClient("mongodb://localhost:27017/") 
db = client["QuantumRelicDB"]
collection = db["chat_history"]

# Rooms dictionary to keep track of active connections
rooms = {}

@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, passcode: str = None):
    await websocket.accept()
    
    if room_id not in rooms:
        rooms[room_id] = []
    
    rooms[room_id].append(websocket)
    
    # --- SEND OLD CHAT HISTORY ON CONNECTION ---
    # Database se is room ki purani saari history nikaal kar user ko bhej rahe hain
    history = collection.find({"room_id": room_id}).sort("timestamp", 1)
    
    for msg in history:
        await websocket.send_json({
            "type": msg.get("type", "message"), 
            "data": msg.get("data", ""), 
            "sender": msg.get("sender", "Partner")
        })

    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # --- SAVE NEW MESSAGE TO MONGODB ---
            document = {
                "room_id": room_id,
                "sender": message_data.get("sender", "Unknown"),
                "data": message_data.get("data", ""),
                "type": message_data.get("type", "message"),
                "timestamp": datetime.now()
            }
            collection.insert_one(document)

            # Broadcast message to everyone else in the room
            for client_ws in rooms[room_id]:
                if client_ws != websocket:
                    await client_ws.send_text(data)
                    
    except WebSocketDisconnect:
        rooms[room_id].remove(websocket)
        if not rooms[room_id]:
            del rooms[room_id] # Memory clean karne ke liye empty room delete kar do