import json
import os
import sys

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "./vendored"))

import requests
from googletrans import Translator

TOKEN = os.environ['TELEGRAM_TOKEN']
BASE_URL = "https://api.telegram.org/bot{}".format(TOKEN)

def translate(text):
    translator = Translator()
    language = translator.detect(text)
    if language.lang == "ru":
        result_translate = translator.translate(text, dest='en')
    elif language.lang == "en":
        result_translate = translator.translate(text, dest='ru')
    else:
        return "Incorrect request";
    return result_translate.text

def send_message(chat_id, text):
    url = BASE_URL + "/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text
    }
    request = requests.post(url, data = data)

def entry_point(event, context):
    data = json.loads(event["body"])

    translate_text = translate(data["message"]["text"])
    send_message(data["message"]["from"]["id"], translate_text)

    return {"statusCode": 200}
