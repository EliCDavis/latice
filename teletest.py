import os

from telegram.ext import CommandHandler, Updater
import time


def should_respond(update, context):

    if update.message.from_user.id == 106468411 or update.message.from_user.id == 498210009:
        return True

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Unauthorized user... if you want to try hacking this, try starting by looking at the source code at: https://github.com/EliCDavis/latice"
    )

    print("Unauthorized Guest {0}-{1}: {2}".format(
        update.message.from_user.username, update.message.from_user.id, update.message.text))

    return False


def remove_prefix(text, prefix):
    if text.lower().startswith(prefix.lower()):
        return text.lower()[len(prefix):].strip()
    return text.lower()  # or whatever

