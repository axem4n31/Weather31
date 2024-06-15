from typing import List

from pydantic import BaseModel, Field

markup_keyboard = {
    "keyboard": [
        [{"text": "Текущая погода 🌡️"}],
        [{"text": "Прогноз погоды 🌤️"}],
        [{"text": "Уведомления 🔔"}, {"text": "Изменить регион 🌍"}, {"text": "Помощь 🆘"}]
    ],
    "resize_keyboard": True
}

get_location_keyboard = {
    "keyboard": [
        [{"text": "Поделиться геолокацией", "request_location": True}]],
    "one_time_keyboard": True,
    "resize_keyboard": True

}


class _UserDataMessage(BaseModel):
    """Базовая модель данных пользователя для типизации сообщений Telegram"""
    id: int
    is_bot: bool
    first_name: str
    last_name: str
    username: str
    language_code: str


class _ChatDataMessage(BaseModel):
    """Базовая модель данных чата для типизации сообщений Telegram"""
    id: int
    first_name: str
    last_name: str
    username: str
    type: str


class _EntityMessage(BaseModel):
    """Базовая модель данных для типизации сообщений Telegram"""
    offset: int
    length: int
    type: str


class _BaseMessage(BaseModel):
    """Базовая модель сообщения для типизации сообщений Telegram"""
    message_id: int
    from_: _UserDataMessage = Field(alias='from')
    chat: _ChatDataMessage
    date: int
    text: str
    entities: List[_EntityMessage]


class UpdateMessage(BaseModel):
    update_id: int
    message: _BaseMessage
