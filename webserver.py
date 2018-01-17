from flask import Flask, render_template, request
import os
import requests
import json
import session

# Create application, and point static path (where static resources like images, css, and js files are stored) to the
# "static folder"
app = Flask(__name__,static_url_path="/static")

@app.route('/browse',methods=['GET'])
def cuisine_display():
	email = session["email"]
	para={'email':email}
    data = requests.get(
        'http://localhost:5001/browse',params=para)
    if data.status_code == requests.codes.ok:
        
		user_data = data.json()
        user1name = user_data['1']['pic1.name']
        user1price = user_data['1']['pic1.price']
        user1food = user_data['1']['pic1.food']
        user1time = user_data['1']['pic1.time']

        user2 = user_data['2']
        user3 = user_data['3']
        user4 = user_data['4']
        user5 = user_data['5']

        pic1 = {
        	'name': user1name
        	'price': user1price
        	'food': user1food
        	'time': user1time
        }	

        return render_template("browse.html",name=user1name,price=user1price,food=user1food,time=user1time)
    else:
        return ("<h1>Error</h1>")


