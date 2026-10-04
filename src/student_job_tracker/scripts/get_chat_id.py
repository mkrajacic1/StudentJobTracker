import dotenv
import requests

import json
import os

UPDATES_POLLING_TIMEOUT = 5

def main():
    dotenv.load_dotenv()

    try:
        TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
        UPDATES_API = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
    except KeyError as exc:
        print("Error occurred while loading the bot token:", repr(exc))
        print("Make sure the telegram bot token variable is correctly set in the .env file")
        return

    print("Obtain the chat ID by messaging your Telegram Bot.")
    input("After messaging the bot, press any key to continue...")
    print()

    # allow response window of double the polling time for slow responses
    request_timeout = UPDATES_POLLING_TIMEOUT * 2
    params = {"timeout": UPDATES_POLLING_TIMEOUT, "offset": -1, "limit": 1, "allowed_updates": json.dumps(["message"])}
    try:
        response = requests.get(UPDATES_API, timeout=request_timeout, params=params)
        response.raise_for_status()
        update = response.json()
    except requests.ReadTimeout:
        print("Request for Bot updates timed out.")
    except requests.JSONDecodeError as exc:
        print("Update response body invalid, couldn't deserialize JSON:", exc)
    except requests.RequestException as exc:
        print("An error occured trying to fetch updates from the Bot:", exc)
    else:
        if not update['result']:
            print("No updates to fetch, possibly try to send another message to the Bot")
        else:
            chat_id = update["result"][0]["message"]["chat"]["id"]
            print("Your chat ID is:", chat_id)
            print("Store the ID in the .env file under: TELEGRAM_CHAT_ID")

    
if __name__ == "__main__":
    main()