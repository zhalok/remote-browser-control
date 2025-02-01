import uuid
from playwright.async_api import async_playwright, Page
from models.session_response import SessionResponse
from store.session import add
from fastapi import APIRouter

browser_router = APIRouter()


@browser_router.post("/start-browser", response_model=SessionResponse)
async def start_browser():
    session_id = str(uuid.uuid4())
    playwright_instance = await async_playwright().start()
    browser = await playwright_instance.chromium.launch(headless=False)
    page = await browser.new_page()
    await page.goto("https://google.com")
    add(session_id, playwright_instance, browser, page)

    return {"sessionId": session_id, "message": "Browser started"}
