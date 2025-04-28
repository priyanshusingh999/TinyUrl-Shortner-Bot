import requests
import time, os
import pyshorteners
from app import *

BOT_TOKEN = os.getenv('BOT_TOKEN')
def get_updates(offset=None):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/getUpdates'
    params = {'offset': offset}
    response = requests.get(url, params=params)
    return response.json()

def send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    response = requests.post(url, data=payload)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def handle_command(command, chat_id, user_info):
    if command.startswith('/start'):
        handle_start(chat_id, user_info)
    elif command.startswith('/help'):
        handle_help(chat_id)
    elif command.startswith('/tinyurl'):
        handle_tinyurl(chat_id, command)
    else:
        send_message(chat_id, "Unknown command. Type /help to see available commands.")

#========================================================================================================================================================================

def handle_start(chat_id, user_info):
    first_name = user_info.get('first_name', '')
    last_name = user_info.get('last_name', '')
    start_text = (
        f"Welcome 🙋 {first_name} {last_name}\n\n"
        "I'm a Link Shortener Bot!\n"
        "Send me one or multiple links after /tinyurl and I'll shorten them for you.\n\n"
        "Type /help to see all commands."
    )
    send_message(chat_id, start_text)

def handle_help(chat_id):
    help_text = (
        'Available commands:\n'
        '/start - Start the bot\n'
        '/help - Help message\n'
        '/tinyurl <link1> <link2> - Get TinyURL short links'
    )
    send_message(chat_id, help_text)

def handle_tinyurl(chat_id, message_text):
    parts = message_text.split(maxsplit=1)
    if len(parts) > 1:
        urls = parts[1].strip().split()
        shortener = pyshorteners.Shortener()
        reply_text = "Here are your shortened URLs:\n\n"
        
        for url in urls:
            try:
                short_url = shortener.tinyurl.short(url)
                reply_text += f"➡️ {short_url}\n"
            except Exception as e:
                reply_text += f"❌ Failed to shorten {url}: {e}\n"
        
        send_message(chat_id, reply_text)
    else:
        send_message(chat_id, "Please provide one or more URLs after /tinyurl command.")

#========================================================================================================================================================================

def main():
    offset = None
    while True:
        updates = get_updates(offset)
        for update in updates.get('result', []):
            if 'message' not in update:
                continue

            chat_id = update['message']['chat']['id']
            message_text = update['message'].get('text', '')
            user_info = update['message'].get('from', {})

            if not message_text:
                continue

            print(f"Received message: {message_text}")

            if message_text.startswith('/'):
                handle_command(message_text, chat_id, user_info)
            else:
                send_message(chat_id, "Please send a valid command or type /help.")

            offset = update['update_id'] + 1

        time.sleep(1)

if __name__ == "__main__":
    main()