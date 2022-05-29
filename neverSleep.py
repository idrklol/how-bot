from flask import Flask
from threading import Thread
import random
import time
import requests
import logging
app = Flask('') #create flask app
@app.route('/')
def home():
    return "I'm up and running!\nhttps://replit.com/@idrklol/howbot" #fancy message

def run():
  app.run(host='0.0.0.0',port=random.randint(2000,9000)) #server port
def ping(target, debug):
    while(True):
        r = requests.get(target)
        if(debug == True):
            print("Status Code: " + str(r.status_code))
        time.sleep(random.randint(180,300)) #alternate ping time between 3 and 5 minutes
def awake(target, debug=False):  
    log = logging.getLogger('werkzeug') #comprehensive WSGI web application library
    log.disabled = True
    app.logger.disabled = True 
    t = Thread(target=run)
    r = Thread(target=ping, args=(target,debug,))
    t.start()
    r.start()