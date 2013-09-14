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

@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/upload',methods=['POST'])
def upload_file():
    # Acquire file from client
    if request.method != "POST":
        return u"Error: Please upload csv file!"
    if upload_file_regex.match(request.form["password"] ):
        password = request.form["password"]
    else:
        return u"Error: Please set password."

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
        print "Storing DB"
        # Drop current all DB.
        session.query(KokmsCore).delete() 
        # Store from csv.
        for d in csv_dict:
            record = KokmsCore(d['date'],d['time'],d['stat'],d['name'],d['mins'])
            session.add(record)
            
    #  if not uploaded, try to fetch from current DB.
    else:
        print "no data."
        for entity in session.query(KokmsCore):
            print "This is", entity.date, entity.time, entity.stat, entity.name, entity.mins
                    
    close_session()
    return "OK"
    
if __name__ == "__main__":
    app.run(debug=True)