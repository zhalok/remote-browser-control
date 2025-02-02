from pydantic import BaseModel
from playwright.async_api import Browser, Page, Playwright


class SessionStore(BaseModel):
    playwright: object
    browser: object
    page: object
