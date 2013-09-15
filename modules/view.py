from flask import Flask;
from flask import render_template
from flask import request

from logic.csvparser import parse_iter
from databases.db import KokmsCore,open_session,close_session

from time import strftime
from random import random 
from hashlib import md5

import os
import re

upload_file_regex = re.compile('[0-9a-zA-Z_-]{1,32}')
app = Flask(__name__)

"""
Initial screen.
"""
@app.route('/')
def index():
    return render_template("index.html")

"""
After uploading csv file (next to the index page).
1. Display error screen with index.html:
    i.  No CSV uploaded && No current DB is found according to password.
    ii. No POST method request(405 Error)
    iii.Other exception regarding CSV parsing
    iv. No password is given.
2. Display filtering screen    
"""
@app.route('/upload',methods=['POST'])
def upload_file():
    # Password check.
    if upload_file_regex.match(request.form["password"] ):
        password = request.form["password"]
    else:
        return u"Error: Please set password."
    # file check.
    f = request.files['csvfile']
    if(f):
        print "file detected."
        file_name = md5(strftime('%Y%m%d%H%M%S') + str(random())).hexdigest()
        file_path = os.path.join(os.getcwd(),"upload/" + file_name)
        f.save(file_path)
        # parse csv
        csv_dict = parse_iter(open(file_path,"r"))

    # DB open 
    session = open_session(password)

    # if CSV is uploaded, store them into databases.
    if(f):
        # Drop current all DB.
        session.query(KokmsCore).delete() 
        # Store from csv.
        for d in csv_dict:
            record = KokmsCore(d['date'],d['time'],d['stat'],d['name'],d['mins'])
            session.add(record)

    # if data is found, pass to next screen.
    if session.query(KokmsCore).count() != 0:
        param = {}
        param['min_date'] = session.query(KokmsCore,func.min(KokmsCore.date)).date
        param['max_date'] = session.query(KokmsCore,func.max(KokmsCore.date)).date
        param['names'] = []
        for username in session.query(KokmsCore).group_by(KokmsCore.username):
            print username

        # Construct dict.
#         for entity in session.query(KokmsCore):
#             print "This is", entity.date, entity.time, entity.stat, entity.name, entity.mins
        #return render_template('selection.html',)

                    
    close_session()
    return "OK"
    
if __name__ == "__main__":
    app.run(debug=True)