import os
from picamera import PiCamera

from telegram.ext import CommandHandler, Updater
import time

camera = PiCamera()

updater = Updater(token=os.environ['TELEGRAM_TOKEN'], use_context=True)
dispatcher = updater.dispatcher


def should_respond(chat_id):
    if chat_id == 106468411:
        return True
    return False


def remove_prefix(text, prefix):
    if text.lower().startswith(prefix.lower()):
        return text.lower()[len(prefix):].strip()
    return text.lower()  # or whatever


def capture_picture_command(update, context):
    camera.capture('./image.jpg')
    print('took picture')
    context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=open('./image.jpg', 'rb')
    )

def capture_video_command(update, context):
    print("starting recording")
    # camera.start_preview()
    camera.start_recording('./video.h264')
    time.sleep(5)
    camera.stop_recording()
    # camera.stop_preview()
    print('took video')
    os.system('MP4Box -add video.h264 video.mp4')
    context.bot.send_video(
        chat_id=update.effective_chat.id,
        video=open('./video.mp4', 'rb')
    )


def set_mode_command(update, context):
    if should_respond(update.effective_chat.id) == False:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Unauthorized user... if you want to try hacking this, try starting by looking at the source code at: https://github.com/EliCDavis/latice"
        )
        print("Unauthorized Guest {0}-{1}: {2}".format(
            update.message.from_user.username, update.message.from_user.id, update.message.text))
        return

    command = remove_prefix(update.message.text, "/mode")
    return_message = "Unrecognized command"

    if command == "twinkle":
        print("Setting mode to twinkle")
        return_message = ""
    elif command == "sleep":
        print("Setting mode to sleep")
        return_message = "Setting mode to sleep"
    elif command == "bug":
        print("Setting mode to lightning bug")
        return_message = "Setting mode to lightning bug"
    elif command == "security":
        print("Setting mode to security")
        return_message = "Setting mode to security"
    elif command == "":
        return_message = "Please Specify a mode [twinkle | bug | security | sleep]"
    else:
        print("Unrecognized command")

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=return_message
    )


dispatcher.add_handler(CommandHandler('picture', capture_picture_command))
dispatcher.add_handler(CommandHandler('video', capture_video_command))
dispatcher.add_handler(CommandHandler('mode', set_mode_command))

if __name__ == '__main__':
    try:
        updater.start_polling()
    except KeyboardInterrupt:
        print("stopping bot")
