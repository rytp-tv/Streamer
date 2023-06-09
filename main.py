import time
import subprocess
import selenium
import requests
import psutil
import shelve
from threading import Thread
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import wordgame

# Параметры запуска FFmpeg
cmds = ['ffmpeg', 
        '-r', '5',
        '-f', 'image2', 
        '-stream_loop', '-1', 
        '-i', 'screen.png',
        '-re', '-stream_loop', '-1',
        '-i', 'music.mp3', 
        '-preset', 'ultrafast', '-tune', 'stillimage', 
        '-vf', 'format=yuv420p',
        '-c:v', 'libx264', '-b:v', '4000k', '-maxrate', '6000k', '-bufsize', '4000k', '-g', '2', 
        '-c:a', 'aac', 
        '-f', 'flv', '-r', '16', 'rtmp://a.rtmp.youtube.com/live2/rb83-ssyw-mt4f-vpg6-2azs', '-loglevel', 'warning']

# Настраиваем Selenium среду для создания снимков страницы

service = Service(ChromeDriverManager().install())

options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--headless")
options.add_argument("window-size=1280,720")
#options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=service, options=options)

def image():
  global timeout
  driver.get('http://youtubestreamer.alwaysdata.net/')
  while True:
    driver.save_screenshot('screen.png')
    #print("Screen...")
    time.sleep(5)

print("Run FFMPEG now...")
subprocess.Popen(cmds)
image()
