import os
import time
import json
import urllib.request
import urllib.parse

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    raise Exception("BOT_TOKEN is not set")

API = f"https://api.telegram.org/bot{TOKEN}"


def telegram(method, data=None):
    url = f"{API}/{method}"

    if data:
        data = urllib.parse.urlencode(data).encode()

    request = urllib.request.Request(url, data=data)

    with urllib.request.urlopen(request) as response:
        return json.loads(response.read().decode())


def send_message(chat_id, text):
    telegram("sendMessage", {
        "chat_id": chat_id,
        "text": text
    })


def main():
    offset = 0

    while True:
        try:
            result = telegram("getUpdates", {
                "offset": offset,
                "timeout": 30
            })

            for update in result.get("result", []):
                offset = update["update_id"] + 1

                message = update.get("message")

                if not message:
                    continue

                chat_id = message["chat"]["id"]
                text = message.get("text", "")

                if text == "/start":
                    send_message(
                        chat_id,
                        "سلام 👋\nربات فعال است. سوال خود را بفرستید."
                    )

                elif text == "/help":
                    send_message(
                        chat_id,
                        "راهنما:\n\n"
                        "/start - شروع ربات\n"
                        "/help - راهنما"
                    )

                elif text:
                    send_message(
                        chat_id,
                        "پیام شما دریافت شد ✅"
                    )

        except Exception as e:
            print("Error:", e)
            time.sleep(5)


if __name__ == "__main__":
    main()
