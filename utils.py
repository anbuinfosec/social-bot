#coding=utf-8
#!/bin/python3
#############################$##############
# PYTHON SOCIAL MEDIA VIDEO DOWNLOADER BOT #
#          BOT VERSION: 1.0.1              #
#  AUTHOR : MOHAMMAD ALAMIN (anbuinfosec)  #
#      GET APIKEY : https://anbusec.xyz    #
#           COPYRIGHT : anbuinfosec        #
############################################
import os
import requests
import re
import random
import string
import psutil
import json
import subprocess
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")


def clear():
  os.system("clear")


def check_tmp():
  tmp_folder = os.path.join(os.getcwd(), 'tmp')
  if not os.path.exists(tmp_folder):
    os.makedirs(tmp_folder)


def get_storage_info():
  try:
    disk_partitions = psutil.disk_partitions()
  except PermissionError:
    print(
        "[!] PermissionError: Unable to access disk partitions. Some information may be unavailable."
    )
    return

  for partition in disk_partitions:
    try:
      partition_info = psutil.disk_usage(partition.mountpoint)
      print(f"[+] Partition: {partition.device}")
      print(f"[+] Total: {partition_info.total} bytes")
      print(f"[+] Used: {partition_info.used} bytes")
      print(f"[+] Free: {partition_info.free} bytes")
      print(f"[+] Percentage Used: {partition_info.percent}%\n")
    except PermissionError:
      print(
          f"[!] PermissionError: Unable to access information for {partition.device}."
      )


def check_system_ip():
  try:
    data = json.loads(requests.get('https://api.myip.com/').text)
    print(f"[+] SERVER COUNTRY : {data['country']}")
    print(f"[+] SERVER IP: {data['ip']}")
  except json.JSONDecodeError:
    print("[!] Error decoding JSON response.")
  except requests.RequestException as e:
    print(f"[!] Request error: {e}")


def random_name():
  random_id = ''.join(random.choice(string.digits) for _ in range(10))
  return f'{random_id}.mp4'


def check_downloader(url):
  facebook_regex = r'(https?://)?(www\.)?(facebook\.com|fb\.watch|fb\.com|m\.facebook\.com|web\.facebook\.com)/.+$'
  youtube_regex = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/.+$'
  terabox_regex = r'(https?://)?(www\.)?teraboxapp\.com/s/.+$'
  instagram_regex = r'(https?://)?(www\.)?instagram\.com/(p|reel|tv)/.+'
  twitter_regex = r'(https?://)?(www\.)?twitter\.com/.+/status/.+'

  if re.match(facebook_regex, url):
    return "facebook"
  elif re.match(youtube_regex, url):
    return "youtube"
  elif re.match(terabox_regex, url):
    return "terabox"
  elif re.match(instagram_regex, url):
    return "instagram"
  elif re.match(twitter_regex, url):
    return "twitter"
  else:
    return False


def downloadFromUrl(url, destination_folder='tmp'):
  response = requests.get(url)
  if response.status_code == 200:
    FileName = random_name()
    file_path = os.path.join(destination_folder, FileName)
    with open(file_path, "wb") as f:
      f.write(response.content)
      print(
          f"[+] FILE DOWNLOADED : {url}\n[+] FILE SAVED : {os.path.join(destination_folder, FileName)}\n=======================================================================\n\n"
      )
      return file_path
  else:
    return False


def get_video_download_info(video_url, downloader):
  base_url = f'https://anbusec.xyz/api/downloader/{downloader}'
  query_params = {'apikey': api_key, 'url': video_url, 'pwd': ''}
  try:
    response = requests.get(base_url, params=query_params)
    response.raise_for_status()
    result = response.json()
    return result
  except requests.exceptions.RequestException as e:
    return {"status": False, "message": f"Error: {e}"}
