import os
from picamera import PiCamera

from telegram.ext import CommandHandler, Updater
import time

camera = PiCamera()


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


def capture_picture_command(update, context):
    if teletest.should_respond(update, context) == False:
        return
    camera.capture('./image.jpg')
    print('took picture')
    context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=open('./image.jpg', 'rb')
    )

def capture_video_command(update, context):
    if teletest.should_respond(update, context) == False:
        return
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


def run_bot():
    updater = Updater(token=os.environ['TELEGRAM_TOKEN'], use_context=True)
    
    updater.dispatcher.add_handler(CommandHandler('picture', capture_picture_command))
    updater.dispatcher.add_handler(CommandHandler('video', capture_video_command))

    updater.start_polling()

if __name__ == '__main__':
    try:
        run_bot()
    except KeyboardInterrupt:
        print("stopping bot")
