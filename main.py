from fastapi import FastAPI

from app.routers import api_router
from telegram_service.routers import event_router, telegram_router
from telegram_service.webhook import set_webhook, remove_webhook

app = FastAPI(
    title="Weather31",
    description="Weather for every day, created by IBD",
)
app.include_router(router=telegram_router)
app.include_router(router=event_router)
app.include_router(router=api_router)


@app.on_event("startup")
async def startup_event():
    await set_webhook()


@app.on_event("shutdown")
async def shutdown_event():
    await remove_webhook()
