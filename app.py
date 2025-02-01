from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from controllers.browser import browser_router
from store.websocket import (
    get as webSocketStoreSet,
    set as webSocketStoreGet,
    delete as webSocketStoreDelete,
)
from store.session import get as sessionStoreGet
import base64
import asyncio
from fastapi.middleware.cors import CORSMiddleware
from store.websocket import set as webSocketSet
import os
import uuid

app = FastAPI()

origins = os.getenv("ALLOWED_ORIGINS").split(",")


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health-check")
async def health_check():
    return {"status": "ok"}


@app.websocket("/stream/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()

    webSocketSet(session_id, websocket)

    while True:
        session = sessionStoreGet(session_id=session_id)
        page = session["page"]

        screenshot = await page.screenshot()
        await websocket.send_bytes(screenshot)
        # encoded_image = base64.b64encode(screenshot).decode("utf-8")
        # await websocket.send_text(f"{encoded_image}")
        # await asyncio.sleep(0.1)

    # try:
    #     while True:
    #         data = await websocket.receive_text()
    #         action = Action.parse_raw(data)
    #         if session_id in sessions:
    #             session = sessions[session_id]
    #             page = session["page"]

    #             # Perform the action from WebSocket client
    #             if action.action == "goto":
    #                 await page.goto(action.payload["url"])
    #                 await websocket.send_text(f"Navigated to {action.payload['url']}")

    #             elif action.action == "click":
    #                 click_request = action.payload
    #                 await page.mouse.click(click_request["x"], click_request["y"])
    #                 await websocket.send_text(
    #                     f"Clicked at ({click_request['x']}, {click_request['y']})"
    #                 )

    #             elif action.action == "type":
    #                 type_request = action.payload
    #                 await page.fill(type_request["selector"], type_request["text"])
    #                 await websocket.send_text(
    #                     f"Typed '{type_request['text']}' in {type_request['selector']}"
    #                 )

    #             else:
    #                 await websocket.send_text("Unknown action")
    #         else:
    #             await websocket.send_text(f"Session {session_id} not found")

    # except WebSocketDisconnect:
    #     webSocketStoreDelete[session_id]
    #     await websocket.close()


app.include_router(browser_router)
