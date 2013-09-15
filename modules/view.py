from flask import Flask;
from flask import render_template
from flask import request
from flask import url_for

from logic.csvparser import parse_iter
from logic.arithmetic import summation 
from databases.db import *
# from models.forms.forms import IndexForm

from time import strftime
from random import random 
from hashlib import md5, sha256 

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
@app.route('/upload', methods=['POST'])
def upload_file():
    # Password check.
    if upload_file_regex.match(request.form["password"]):
        password = sha256(request.form["password"]).hexdigest()
    else:
        return u"Error: Please set password."
    # file check.
    f = request.files['csvfile']
    if(f):
        print "file detected."
        file_name = md5(strftime('%Y%m%d%H%M%S') + str(random())).hexdigest()
        file_path = os.path.join(os.getcwd(), "upload/" + file_name)
        f.save(file_path)
        # parse csv
        csv_dict = parse_iter(open(file_path, "r"))

    # DB open 
    session = open_session(password)

    # if CSV is uploaded, store them into databases.
    if(f):
        # Drop current all DB.
        session.query(KokmsCore).delete() 
        # Store from csv.
        for d in csv_dict:
            record = KokmsCore(d['date'], d['time'], d['stat'], d['name'], d['mins'])
            session.add(record)

    # if data is found, pass to next screen.
    if session.query(KokmsCore).count() != 0:
        param = {}
        names = [x for x in iterator_name(session)] 
        dates = [x for x in iterator_existing_dates(session)]
        close_session()
        return render_template('selection.html'\
                               , names=names\
                               , dates=dates, \
                                password=password)

    # Otherwise, please upload CSV!
    return "Please upload CSV!"

@app.route('/display_meisai', methods=['POST'])
def display_meisai():
    if request.form['password']:
        session = open_session(request.form['password'])
    else :
        # CSRF
        return redirect(url_for('index'))

    # Filter by name and price. 
    filtered_entities = filterby_name_date(session, \
                       request.form['target'], \
                       request.form['begindate'], \
                       request.form['enddate'])
    # Summarize
    summarized_data = summarize(filtered_entities)
    
    if request.form['rate']:
        rate = float(request.form['rate'])  
        rate_input = True
        if rate <= 0: rate_input = False
    else:
        rate = 0.0
        rate_input = False

    metadata = summation(summarized_data, int(request.form['price']), rate)
    
    # Output.
#     import pdb
#     pdb.set_trace()
    return render_template("meisai.html",\
                            name = request.form['target'],\
                            rate = request.form['rate'],\
                            title = request.form['title'],\
                            price = request.form['price'],\
                            summarize = summarized_data,\
                            metadata = metadata, \
                            rate_input = rate_input)
    
if __name__ == "__main__":
    app.run(debug=True)