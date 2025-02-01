from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from controllers.browser import browser_router
from store.session import get as sessionStoreGet
import base64
import asyncio
from fastapi.middleware.cors import CORSMiddleware
from store.websocket import set as webSocketSet
import os
import traceback
import json
from playwright.async_api import Page


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


async def stream_browser_session(page: Page, websocket):
    while True:
        try:
            screenshot = await page.screenshot()
            await websocket.send_bytes(screenshot)
        except Exception:
            traceback.print_exc()


async def handle_interaction(page: Page, interaction, websocket):

    # Perform the action from WebSocket client
    # if interaction.action == "goto":
    #     await page.goto(interaction.payload["url"])
    #     await websocket.send_text(f"Navigated to {interaction.payload['url']}")
    print("interaction", interaction)
    if interaction["action"] == "click":
        click_request = interaction["payload"]
        viewport_size = await page.evaluate(
            "({width: window.innerWidth, height: window.innerHeight})"
        )
        playwright_width = viewport_size["width"]
        playwright_height = viewport_size["height"]
        click_x = click_request["x"]
        click_y = click_request["y"]
        frame_width = click_request["fw"]
        frame_height = click_request["fh"]
        click_x = click_x * (playwright_width / frame_width)
        click_y = click_y * (playwright_height / frame_height)

        # page.mouse.click(click_request["x"], click_request["y"])
        await page.mouse.click(click_x, click_y)
        # await stream_browser_session(page=page, websocket=websocket)
        # await websocket.send_text(
        #     f"Clicked at ({click_request['x']}, {click_request['y']})"
        # )

    # elif interaction.action == "type":
    #     type_request = interaction.payload
    #     await page.keyboard.type(type_request["text"])
    #     await websocket.send_text(f"Typed {type_request['text']}")


@app.websocket("/stream/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()

    webSocketSet(session_id, websocket)
    session = sessionStoreGet(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")
    page = session["page"]

    while True:
        asyncio.create_task(stream_browser_session(page, websocket))
        data = await websocket.receive_text()
        event = json.loads(data)
        await handle_interaction(page=page, interaction=event, websocket=websocket)

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
