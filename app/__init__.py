'''
At the command line, run 
conda activate PIC16B
export FLASK_ENV=development
flask run
'''

from flask import Flask, g, render_template, request
import numpy as np
import sqlite3

app = Flask(__name__)

@app.route("/") 
def base():
    return render_template("base.html")

def get_message_db():
    try:
        return g.message_db
    except:
        #create our table
        g.message_db = sqlite3.connect("messages_db.sqlite")
        cmd = \
        '''
        CREATE TABLE IF NOT EXISTS `messages` (
            id  INTEGER PRIMARY KEY AUTOINCREMENT  ,
            name TEXT NOT NULL,
            message TEXT NOT NULL
        );
        '''
        cursor = g.message_db.cursor()
        cursor.execute(cmd)

        return g.message_db

def insert_message():
    #get message and name inputted by user
    message = request.form['message']
    name = request.form['name']

    #open connection to database
    conn = get_message_db()

    #insert into our database
    cmd = \
    f'''
    INSERT INTO messages (name, message) VALUES ('{name}', '{message}');
    '''
    cursor = conn.cursor()
    cursor.execute(cmd)
    conn.commit()
    conn.close()

    return name, message


@app.route("/submit/", methods=['POST', 'GET'])
def submit():
    if request.method == 'GET':
        # if the user just visits the url
        return render_template('submit.html')
    else:
        try:
            # if the user submits the form, call on insert_message, which will put input into database
            name, message = insert_message()
            # if user submits
            return render_template('submit.html', submit=True, message=message, name=name)
        except:
            return render_template('submit.html', error=True)

def random_messages(n):
    # refer to insert_messages and discussion view function 
    # HINT SQL command - ORDER BY RANDOM()

    #connect database
    conn = get_message_db()

    #SQL command
    cmd = \
    f'''
    SELECT * FROM messages ORDER BY RANDOM() LIMIT {n}

    '''

    cursor = conn.cursor()
    #take out SQL command and execute it
    cursor.execute(cmd)
    all_msg = cursor.fetchall()
    conn.close()

    return  all_msg

@app.route('/view/')
def view():

    #call on random_messages() function
    return render_template('view.html', messages= random_messages(5))
