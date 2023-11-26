#coding=utf-8
#!/bin/python3
#############################$##############
# PYTHON SOCIAL MEDIA VIDEO DOWNLOADER BOT #
#          BOT VERSION: 1.0.1              #
#  AUTHOR : MOHAMMAD ALAMIN (anbuinfosec)  #
#      GET APIKEY : https://anbusec.xyz    #
#           COPYRIGHT : anbuinfosec        #
############################################
import logging
from dotenv import load_dotenv
import os
import telebot
import subprocess
from utils import *
from time import sleep

load_dotenv()
bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
logging.basicConfig(level=logging.INFO)
bot = telebot.TeleBot(bot_token)


def laodInfo():
  print(f"[+] TOKEN LOADED : {bot_token}")
  print(f'[+] APIKEY LOADED : {os.getenv("API_KEY")}')


def start_flask():
  clear()
  subprocess.Popen(["python", "app.py"])
  sleep(1)
  laodInfo()
  check_system_ip()
  print("============================================================")


@bot.message_handler(func=lambda message: True)
def handle_message(message):
  try:
    check_tmp()
    url = message.text
    user_id = message.from_user.id
    chat_id = message.chat.id
    print(
        f"[NEW MESSAGE]==========================================================\n[+] USER ID: [{user_id}]\n[+] CHAT ID: [{chat_id}]\n[+] MESSAGE: {url}"
    )

    wait_message = bot.reply_to(
        message, "⏳ Please wait, trying to download your video...")
    downloader = check_downloader(url)

    if not downloader:
      bot.edit_message_text(
          text=
          "❎ Please enter a valid (YouTube, Facebook, Instagram, Twitter, Terabox) video url.",
          chat_id=chat_id,
          message_id=wait_message.message_id)
      return

    download_info = get_video_download_info(url, downloader)

    if download_info["status"]:
      download_url = download_info.get("url", "")
      video_path = downloadFromUrl(download_url)

      try:
        bot.edit_message_text(text="✅ Video download successful.",
                              chat_id=chat_id,
                              message_id=wait_message.message_id)
      finally:
        if os.path.exists(video_path):
          bot.send_chat_action(message.chat.id, 'upload_video')
          bot.edit_message_text(text="⏳ Please wait, uploading your video...",
                                chat_id=chat_id,
                                message_id=wait_message.message_id)
          video = open(video_path, 'rb')
          bot.send_video(chat_id, video)
          try:
            bot.delete_message(chat_id, wait_message.message_id)
          except telebot.apihelper.ApiException as e:
            print(f'[+] ERROR {e}')
          bot.reply_to(
              message,
              'Thanks for using our bot 💮😍\nJoin our public channel @anbudevs')
          os.remove(video_path)
        else:
          bot.edit_message_text(text="❎ Video not found on path!",
                                chat_id=chat_id,
                                message_id=wait_message.message_id)
    else:
      bot.send_message(message.chat.id,
                       "❎ Server error: Unable to download your video.")

  except Exception as e:
    print(f"[+] ERROR FOUND : {e}")
    logging.error(f"An error occurred: {e}")
    bot.edit_message_text(
        text="✅ An unexpected error occurred. Please try again later.",
        chat_id=chat_id,
        message_id=wait_message.message_id)


if __name__ == '__main__':
  start_flask()
  bot.polling(none_stop=True)
