from app.message.models import BotMessage, MarkupData


def test_bot_message_builds_inline_keyboard():
    markup = MarkupData.from_row_callbacks(
        [("First", "first"), ("Second", "second")],
        [("Third", "third")],
    )

    kwargs = BotMessage(text="Choose", markup=markup).to_aiogram_kwargs()

    rows = kwargs["reply_markup"].inline_keyboard
    assert [[button.text for button in row] for row in rows] == [
        ["First", "Second"],
        ["Third"],
    ]
    assert [[button.callback_data for button in row] for row in rows] == [
        ["first", "second"],
        ["third"],
    ]


def test_bot_message_omits_markup_when_absent():
    kwargs = BotMessage(text="Hello").to_aiogram_kwargs()

    assert kwargs == {"text": "Hello", "parse_mode": None}
