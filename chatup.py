from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from gevent.pywsgi import WSGIServer
from gevent.monkey import patch_all
import requests
import logging
import sys
import argparse
import os
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

parser = argparse.ArgumentParser()
parser.add_argument("--ps", type=int, default = 7320, help="Port of Server running")
parser.add_argument("--pr", type=int, default = 7321, help="Port of API rasa")

args = parser.parse_args()
print (args.ps)

@app.route( '/' )
def hello():
	return render_template( 'ChatApp.html' )

def messageRecived():
	print( 'message was received!!!' )

@socketio.on( 'my event' )
def handle_my_custom_event( json ):
	# request to rasa api
	data = {"sender": "hungdv1234", "message": "đồng ý"}
	data["sender"] = json.get("sender")
	data["message"] = json.get("message")
	# print (data)
	# r = requests.post("http://localhost:"+args.pr+"/webhooks/rest/webhook", json = data, headers={'Content-Type': 'application/json'})
	# print (r.json())
	# # print( 'recived my event: ' + str( json ) )
	# json["message"] = r.json()[0].get("text")
	# json["user_name"] = "Bot: "
	json["message"] = "Hellow"
	json["user_name"] = "Bot: "
	socketio.emit( 'my response', json, callback=messageRecived )

if __name__ == '__main__':
	socketio.run(app, port=7320, host = "127.0.0.1" ,debug = True)
