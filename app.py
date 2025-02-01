from fastapi import FastAPI
from controllers.browser import browser_router

app = FastAPI()


@app.get("/health-check")
async def health_check():
    return {"status": "ok"}


app.include_router(browser_router)
