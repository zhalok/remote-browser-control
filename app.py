from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from playwright.async_api import async_playwright
import uuid
import asyncio

app = FastAPI()


@app.get("/health-check")
async def health_check():
    return {"status": "ok"}
