import json
from pprint import pprint

import requests
from SaitamaRobot import dispatcher
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

# Open API key
GRAMMAR_API_KEY = "6ae0c3a0-afdc-4532-a810-82ded0054236"
URL = "http://services.gingersoftware.com/Ginger/correct/json/GingerTheText"


def translate(update: Update, context: CallbackContext):
    if update.effective_message.reply_to_message:
        msg = update.effective_message.reply_to_message

        params = dict(
            lang="US",
            clientVersion="2.0",
            apiKey=GRAMMAR_API_KEY,
            text=msg.text)

        res = requests.get(URL, params=params)
        # print(res)
        # print(res.text)
        #pprint(json.loads(res.text))
        changes = json.loads(res.text).get('LightGingerTheTextResult')
        curr_string = ""

        prev_end = 0

        for change in changes:
            start = change.get('From')
            end = change.get('To') + 1
            suggestions = change.get('Suggestions')
            if suggestions:
                sugg_str = suggestions[0].get(
                    'Text')  # should look at this list more
                curr_string += msg.text[prev_end:start] + sugg_str

                prev_end = end

        curr_string += msg.text[prev_end:]
        # print(curr_string)
        update.effective_message.reply_text(curr_string)


__help__ = """
 • Replying `/t` to a message will produce the grammar corrected version of it.
"""

__mod_name__ = "Grammar Correction"

TRANSLATE_HANDLER = CommandHandler('t', translate)

dispatcher.add_handler(TRANSLATE_HANDLER)
