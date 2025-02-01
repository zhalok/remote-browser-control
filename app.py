from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from controllers.browser import browser_router
from store.session import get as sessionStoreGet, remove as sessionStoreRemove
import base64
import asyncio
from fastapi.middleware.cors import CORSMiddleware
from store.websocket import set as webSocketSet, delete as webSocketStoreDelete
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
    if interaction["action"] == "goto":
        goto_request = interaction["payload"]
        print("goto_request", goto_request)
        # try:
        #     await page.goto(goto_request["url"])
        # except Exception:
        #     print("error while handling go to operation")
        #     traceback.format_exc()
        await page.goto(goto_request["url"])
        # print("interaction", interaction)
    elif interaction["action"] == "click":
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
        await page.mouse.click(click_x, click_y)

        # await page.goto(goto_request["url"])

    elif interaction["action"] == "type":
        type_request = interaction["payload"]
        if type_request["text"] == "\n":
            await page.keyboard.press("Enter")
        elif type_request["text"] == "Backspace":
            await page.keyboard.press("Backspace")
        else:
            await page.keyboard.press(type_request["text"])

    elif interaction["action"] == "scroll":
        scroll_request = interaction["payload"]
        await page.mouse.wheel(scroll_request["dx"], scroll_request["dy"])


@app.websocket("/stream/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()
    try:

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

    except WebSocketDisconnect:
        webSocketStoreDelete[session_id]
        session = sessionStoreGet(session_id)
        browser = session["browser"]
        await browser.close()
        await websocket.close()


app.include_router(browser_router)
