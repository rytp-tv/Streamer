import time
import subprocess
import selenium
import requests
import psutil
import shelve
from flask import Flask
from flask import request, render_template, jsonify
from threading import Thread
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import wordgame

db = shelve.open('dbm.ndbm', writeback=True)
db["admin"] = {'username': 'admin','count':1}

result = ""
all_count = 0
timeout = 0
last_answer = ""
curr_quest = ""
for i in db:
  all_count += db[i]['count']

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
        '-c:v', 'libx264', '-b:v', '4000k', '-maxrate', '5000k', '-bufsize', '1000k', '-g', '6', 
        '-c:a', 'aac', 
        '-f', 'flv', '-r', '12', 'rtmp://a.rtmp.youtube.com/live2/u6kx-44tt-x9xw-j74y-79pw', '-loglevel', 'warning']

# Настраиваем таймер для викторины
#def quest_timer():
  

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
  driver.get('https://youtubetreamer.onrender.com/')
  while True:
    driver.save_screenshot('screen.png')
    print("Screen...")
    time.sleep(5)
    timeout += 5

print("Run FFMPEG now...")
subprocess.Popen(cmds)

#Настраиваем сервер Flask
app = Flask('')
@app.route("/")
def index():
  if ("ffmpeg" in (i.name() for i in psutil.process_iter())) == False:
    print("Running FFmpeg...")
    return render_template("index.html")
  else:
    return render_template("index.html")

# Обработка JSON-запросов
@app.route('/post_json', methods=['POST'])
def process_json():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        print(json)
        return json
    else:
        return 'Content-Type not supported!'

@app.route('/set_board', methods=['GET'])
def set_board():
  global all_count
  if request.args['user_id'] in db:
    #print("UserID already exists")
    db[request.args['user_id']]["count"] +=1
    db.sync()
    #print(f"{db[request.args['user_id']]['username']} likes is {db[request.args['user_id']]['count']}")
    #print(sorted(db, key=lambda x: db[x]['count'], reverse=True))
    '''
    for i in db:
      print(db.get(i))
      print(db[i]["username"])
      print(db[i]['count'])
    '''
    all_count += 1
    return jsonify(str(db[request.args['user_id']]['count']))
  else:
    db[request.args['user_id']] = {'username':request.args['username'],'count':1}
    db.sync()
    print(db[request.args['user_id']]['count'])
    return jsonify(str(db[request.args['user_id']]['count']))

@app.route('/get_board', methods=['GET'])
def get_board():
  list = sorted(db, key=lambda x: db[x]['count'], reverse=True)
  stats = ''
  for i in list[:20]:
    stats += '<div class="avatar" id="' + i + '" style="width:' + str((5+((db[i]['count']*100)/all_count)*0.15)) + '%"> <img src="https://picsum.photos/seed/'+str(i)+'/200/200"> <span class="text" id="text">' + db[i]["username"] +'</span><span class="num">'+ str(db[i]['count']) +'</span></div>'
  #print(f"Всего голосов: {all_count}")
  return stats

@app.route('/answer', methods=['GET'])
def check_answer():
  global curr_quest
  global last_answer
  answ = request.args['answer']
  name = db[request.args['user_id']]['username']
  if curr_quest != "" and curr_quest != "empty":
    if request.args['user_id'] in db:
      if last_answer != answ and answ == curr_quest[1]:
        db[request.args['user_id']]["count"] +=10
        db.sync()
        last_answer = answ
        wordgame.delete('*'.join(curr_quest))
        return jsonify("@"+name+", Верно!")
      elif last_answer == answ:
        return jsonify("@"+name+", Уже отвечали, дождитесь нового вопроса...")
      elif answ != curr_quest:
        return jsonify("@"+name+", Неверно...")
    else:
      db[request.args['user_id']] = {'username':request.args['username'],'count':1}
      db.sync()
      if last_answer != answ and answ == curr_quest[1]:
        db[request.args['user_id']]["count"] +=9
        db.sync()
        last_answer = answ
        wordgame.delete('*'.join(curr_quest))
        return jsonify("@"+name+", Верно!")
      elif last_answer == answ:
        return jsonify("Уже отвечали, дождитесь нового вопроса...")
      elif answ != curr_quest:
        return jsonify("@"+name+", Неверно...")
  else:
    return jsonify("Новых вопросов пока нет...")

@app.route('/get_question', methods=['GET'])
def get_question():
  global result
  global timeout
  global curr_quest
  if timeout < 120:
    return result + '<div id="countdownExample"><div class="values">'+time.strftime("%M:%S", time.gmtime(timeout))+'</div></div>'
  else:
    curr_quest = wordgame.generate()
    timeout = 0
    if curr_quest != "empty":
      result = '<span class="quest" style="margin-right:15px">' + curr_quest[0] + '</span>'
      for i in curr_quest[1]:
        result += '<div class="letter-box"></div>'
      result += '<script>var timer = new Timer();timer.start({countdown: true, startValues: {seconds: 60}});$("#countdownExample .values").html(timer.getTimeValues().minutes.toString() + ":" + timer.getTimeValues().seconds.toString());timer.addEventListener("secondsUpdated", function (e) {$("#countdownExample .values").html(timer.getTimeValues().minutes.toString() + ":" + timer.getTimeValues().seconds.toString());});timer.addEventListener("targetAchieved", function (e) {$("#countdownExample .values").html("Время истекло...");});</script>'
    else:
     result = '<span class="quest" style="margin-right:15px">Пока новых вопросов нет...</span>'
  return result

@app.route('/check_page', methods=['GET'])
def check_page():
  return "Ok!"

def run():
  app.run(host='0.0.0.0', port=80)

# Запуск записи
screen = Thread(target=image)
screen.start()

# Запуск сервера

app.run(host='0.0.0.0', port=80)

#server = Thread(target=run)
#server.start()
