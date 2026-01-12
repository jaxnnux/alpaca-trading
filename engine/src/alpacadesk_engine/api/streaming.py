"""Real-time data streaming API endpoints"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List, Set
import json
import asyncio

from .auth import get_current_client

router = APIRouter()

# Active WebSocket connections
active_connections: Set[WebSocket] = set()

# Subscribed symbols
subscribed_symbols: Set[str] = set()


def quote_callback(quote_data: dict):
    """
    Callback function for quote updates
    Broadcasts to all connected WebSocket clients
    """
    # Send to all active connections
    for connection in active_connections:
        try:
            asyncio.create_task(
                connection.send_json({
                    "type": "quote",
                    "data": quote_data
                })
            )
        except Exception as e:
            print(f"Error sending quote: {e}")


@router.websocket("/ws/quotes")
async def websocket_quotes(websocket: WebSocket):
    """
    WebSocket endpoint for real-time quote streaming

    Clients can send JSON messages to subscribe/unsubscribe:
    {"action": "subscribe", "symbols": ["AAPL", "MSFT"]}
    {"action": "unsubscribe", "symbols": ["AAPL"]}
    """
    await websocket.accept()
    active_connections.add(websocket)

    try:
        client = get_current_client()
        broker = getattr(client, '_broker', None)

        if not broker:
            await websocket.send_json({
                "type": "error",
                "message": "Broker not available"
            })
            return

        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message = json.loads(data)

            action = message.get("action")
            symbols = message.get("symbols", [])

            if action == "subscribe":
                # Subscribe to new symbols
                for symbol in symbols:
                    if symbol not in subscribed_symbols:
                        subscribed_symbols.add(symbol)

                # Update broker subscription
                if subscribed_symbols:
                    broker.subscribe_quotes(list(subscribed_symbols), quote_callback)

                await websocket.send_json({
                    "type": "subscribed",
                    "symbols": list(subscribed_symbols)
                })

            elif action == "unsubscribe":
                # Unsubscribe from symbols
                for symbol in symbols:
                    subscribed_symbols.discard(symbol)

                if symbols:
                    broker.unsubscribe_quotes(symbols)

                await websocket.send_json({
                    "type": "unsubscribed",
                    "symbols": symbols
                })

    except WebSocketDisconnect:
        active_connections.discard(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        await websocket.send_json({
            "type": "error",
            "message": str(e)
        })
    finally:
        active_connections.discard(websocket)


@router.get("/streaming/status")
async def get_streaming_status():
    """
    Get current streaming status
    """
    return {
        "active_connections": len(active_connections),
        "subscribed_symbols": list(subscribed_symbols),
    }
