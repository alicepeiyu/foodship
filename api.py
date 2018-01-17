from flask import Flask, request, render_template
import json
import sqlite3
import numpy as np

def get_connection():
    return sqlite3.connect('foodship.db')

app = Flask(__name__)

@app.route('/browse',methods=["GET"])
def get_dining_option():
    conn = get_connection()
    c = conn.cursor()

    request_data = request.get_json()
    email = request_data["email"]


    c.execute("SELECT firstName,pref_1,pref_2,pref_3 FROM user WHERE email = '%s'" % email)
    user_data = c.fetchall()

    cuisine = user_data[0][1:]   

    c.execute("SELECT firstName,cuisine,budget,day From dining_option WHERE status = 'unmatched' AND (cuisine = '%s' OR cuisine = '%s' OR cuisine = '%s')" % (cuisine[0],cuisine[1],cuisine[2]))
    lst = c.fetchall()
    # idx: the index of all dining options qualified for recommendation
    idx = np.arange(len(lst))
    np.random.shuffle(idx)
    # idx_chosen: 5 indices chosen
    idx_chosen = idx[:5]


    dining_chosen = [lst[i] for i in idx_chosen]
    user = dict()
    for i in range(0,5):
        user[i+1] = {"pic{}.name".format(i+1): dining_chosen[i][0],
        "pic{}.price".format(i+1): dining_chosen[i][2],
        "pic{}.food".format(i+1): dining_chosen[i][1],
        "pic{}.time".format(i+1): dining_chosen[i][3],
        }

    return json.dumps(user)
