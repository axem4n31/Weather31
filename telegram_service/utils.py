markup_keyboard = {
    "keyboard": [
        [{"text": "Текущая погода 🌡️"}],
        [{"text": "Прогноз погоды 🌤️"}],
        [{"text": "Уведомления 🔔"}, {"text": "Изменить регион 🌍"}, {"text": "Помощь 🆘"}]
    ],
    "resize_keyboard": True
}
markup_inline_get_location = {
    "inline_keyboard": [
        [
            {
                "text": "Поделиться геолокацией",
                "callback_data": "share_location",
                "request_location": True
            }
        ]
    ]
}
get_location_keyboard = {
        "keyboard": [
                [{"text": "Поделиться геолокацией", "request_location": True}]],
        "one_time_keyboard": True,
        "resize_keyboard": True

}

