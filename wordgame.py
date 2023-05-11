import time
import json
import random

questions = {
   "Это что-то зелёное:": [
      "огурец",
      "трава",
      "дерево",
      "яблоко",
      "капуста",
      "арбуз",
      "змея",
      "кактус",
      "хвоя",
     "чай",
     "изумруд",
     "топаз",
     "краска",
     "горошек",
     "ель",
     "салат",
     "лужайка",
     "щи",
     "свет",
     "крокодил",
     "змея",
     "хризоберилл"
   ],
   "Это что-то холодное:": [
      "лёд",
      "снег",
      "погода",
      "сердце",
      "разум",
      "вода",
      "азот",
      "мороженое",
      "погода",
      "взгляд",
      "зима",
      "темперамент",
      "душа",
     "утро",
     "лужа",
     "вода",
     "воздух",
     "земля",
     "еда",
     "переулок",
     "папоротник"
   ],
   "Что никогда не падает?": [
     "неваляшка",
     "звезда",
     "пустота"
   ],
   "Нет серебра и золота, но у меня есть зубы .": [
     "гребень"
   ],
   "Я являюсь зеркалом, но в меня не смотрятся.": [
     "фотоаппарат"
   ]
}

def generate():
  filename = 'quests.txt'
  with open(filename) as file:
    lines = file.read().splitlines()
  if len(lines) > 0:
    random_line = lines[random.randint(0, len(lines)-1)]
    if random_line != "":
      print(random_line.split("*"))
      return random_line.split("*")
    else:
      #print("Нет загадок!")
      return "empty"
  else:
    #print("Нет загадок...")
    return "empty"

def delete(string):
  filename = 'quests.txt'
  with open(filename) as file:
    lines = file.read().splitlines()
  if len(lines) > 0:
    with open(filename, 'w') as output_file:
      output_file.writelines(line + "\n"
                               for line in lines if line != string)
  else:
    pass
    #print("Нет загадок...")

'''
d = {}
  with open("file.txt") as f:
    for line in f:
      (key, val) = line.split()
      d[int(key)] = val
      print(d[int(key)])
  print(d)
'''

if '__main__' == __name__:
  print('Запущен напрямую...?')