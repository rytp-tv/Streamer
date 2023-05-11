from replit import db

#del db['UCIMP28D6SODo8TXOBDGXBWw']
#del db['$(userid)']

for i in db:
  print(i)
  print(db[i]['username'])
