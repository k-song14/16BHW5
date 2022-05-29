'''
At the command line, run 
conda activate PIC16B
export FLASK_ENV=development
flask run

'''

from flask import Flask, g, render_template, request
from flask import redirect, url_for, abort
import numpy as np
import sqlite3

app = Flask(__name__)

@app.route("/") 
def base():
    return render_template("base.html")

@app.route("/submit/", methods=['POST', 'GET'])
def submit():
    if request.method == 'POST':
        # if the user just visits the url
        return render_template('submit.html')
    else:
        try:
            # if the user submits the form
            message = request.form['message']
            name = request.form['name']
            # call the database function if successful submission
            return render_template('submit.html', message=message, name=name)
        except:
            return render_template('submit.html', error=True)

def get_message_db():
    try:
        return g.message_db
    except:
        g.message_db = sqlite3.connect("messages_db.sqlite")
        cmd = \
        '''
        CREATE TABLE IF NOT EXISTS `messages` (
            id INTEGER PRIMARY KEY AUTOINCREMENT  ,
            name TEXT NOT NULL,
            message TEXT NOT NULL
        );
        '''
        cursor = g.message_db.cursor()
        cursor.execute(cmd)
        return g.message_db

def insert_message(request):
    conn = get_message_db()
    cmd = \
    f'''
    INSERT INTO messages
    VALUES (name, message);
    '''
    cursor = conn.cursor()
    cursor.execute(cmd)
    conn.commit()
    conn.close()

@app.route('/view/')
def view():

    #render template
    #return render_template('view.html', messages = random_messages(5))
    #db = get_message_db()

    #SQL command
    #messages = db.execute("SELECT message FROM messages").fetchall()
    return render_template('view.html')

#def random_messages(n):
    # refer to insert_messages and discussion view function 
    # HINT SQL command - ORDER BY RANDOM()

    #connect database
    #db = get_message_db()

    #SQL command
    #messages = db.execute("SELECT * FROM").fetchall()