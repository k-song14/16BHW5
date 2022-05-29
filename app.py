'''
At the command line, run 
conda activate PIC16B
export FLASK_ENV=development
flask run

'''

from flask import Flask, render_template, request
from flask import redirect, url_for, abort

app = Flask(__name__)

@app.route("/") 
def base():
    return render_template("base.html")

@app.route("/submit/", methods=['POST', 'GET'])
def ask():
    if request.method == 'GET':
        # if the user just visits the url
        return render_template('submit.html')
    else:
        # if the user submits the form
        message = request.form['message']
        name = request.form['name']
        return render_template('submit.html', message=message, name=name)

@app.route("/view/")
def view():
    return render_template("view.html")