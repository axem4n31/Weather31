from fastapi import APIRouter, Request

from handly_event import handle_bot_events

event_router = APIRouter(prefix="/handle_bot_events", tags=["Handle events"])
api_router = APIRouter(prefix="/api", tags=["API"])


@event_router.post('/{secret_key:str}/')
async def handle_bot_events_router(request: Request, secret_key: str):
    await handle_bot_events(request=request, secret_key=secret_key)


@api_router.get('/test/{vol:int}')
async def test(vol: int):
    return vol * 5
