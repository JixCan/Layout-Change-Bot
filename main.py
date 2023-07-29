import telebot
from background import keep_alive
import config

keyboard_layout = {
    "a": "ф",
    "b": "и",
    "c": "с",
    "d": "в",
    "e": "у",
    "f": "а",
    "g": "п",
    "h": "р",
    "i": "ш",
    "j": "о",
    "k": "л",
    "l": "д",
    "m": "ь",
    "n": "т",
    "o": "щ",
    "p": "з",
    "q": "й",
    "r": "к",
    "s": "ы",
    "t": "е",
    "u": "г",
    "v": "м",
    "w": "ц",
    "x": "ч",
    "y": "н",
    "z": "я",
    ",": "б",
    ".": "ю",
    "/": ".",
    "\\": "\\",
    "[": "х",
    "]": "ъ",
    ";": "ж",
    "'": "э",
    "`": "ё",
}

# Создание обратного словаря
reverse_keyboard_layout = {v: k for k, v in keyboard_layout.items()}

# Создание словарей для переключения больших символов
keyboard_layout_uppercase = {k.upper(): v.upper() for k, v in keyboard_layout.items()}
keyboard_layout_uppercase_eng = {
    k.upper(): v.upper() for k, v in keyboard_layout.items()
}
reverse_keyboard_layout_uppercase = {
    v.upper(): k.upper() for k, v in keyboard_layout.items()
}
reverse_keyboard_layout_uppercase_eng = {
    v.upper(): k.upper() for k, v in keyboard_layout.items()
}

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(content_types=["text"])
def get_text_messages(message):
    if message.text.lower() == "/start" or message.text.lower() == "/help":
        bot.send_message(
            message.from_user.id,
            text="Привет! Отправь мне своё сообщение, которое нужно перевести на другую раскладку, и я это сделаю :)",
        )
        return

    original_text = message.text
    eng_to_rus_text = "".join(
        keyboard_layout.get(symbol.lower(), symbol)
        if symbol.islower()
        else keyboard_layout_uppercase.get(symbol, symbol)
        if symbol.isupper()
        else keyboard_layout_uppercase_eng.get(symbol, symbol)
        for symbol in original_text
    )
    rus_to_eng_text = "".join(
        reverse_keyboard_layout.get(symbol.lower(), symbol)
        if symbol.islower()
        else reverse_keyboard_layout_uppercase.get(symbol, symbol)
        if symbol.isupper()
        else reverse_keyboard_layout_uppercase_eng.get(symbol, symbol)
        for symbol in original_text
    )
    swap_all_text = "".join(
        keyboard_layout.get(symbol.lower(), reverse_keyboard_layout.get(symbol, symbol))
        if symbol.islower()
        else keyboard_layout_uppercase.get(
            symbol, reverse_keyboard_layout_uppercase.get(symbol, symbol)
        )
        for symbol in original_text
    )

    response = f"*Ваше оригинальное сообщение:*\n`{original_text}`\n\nСмена английской раскладки на русскую:\n`{eng_to_rus_text}`\n\nСмена русской раскладки на английскую:\n`{rus_to_eng_text}`\n\nСмена всех символов на их аналоги:\n`{swap_all_text}`"

    bot.send_message(message.from_user.id, response, parse_mode="Markdown")


keep_alive()
bot.polling(none_stop=True, interval=0)
