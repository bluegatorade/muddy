#!/usr/bin/python3
import requests
from flask import Flask, session, render_template, request, url_for, flash, redirect
from datetime import datetime
from res_config import ResConfig

app = Flask(__name__)
API_URL = "http://localhost:80"

@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        date = request.form.get('date')
        size = request.form.get('size')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        phone = request.form.get('phone')
        email = request.form.get('email')

        try: 
            res = ResConfig(date, size, firstname, lastname, phone, email)
        except ValueError as e:
            return redirect(url_for('index', message=str(e)))

        try: 
            resp = requests.post(API_URL, data={'res': str(res)})
            if resp.text != "scheduled":
                return redirect(url_for('index', message=resp.text))
        except ConnectionError as e:
            return redirect(url_for('index', message="could not connect to backend"))
        except Exception as e:
            return redirect(url_for('index', message="unknown error"))

        return redirect(url_for('index', message="scheduled"))

    message = ""
    if 'message' in request.args:
        message = request.args['message']
        invalid = False
        for c in message:
            if c.isalpha():
                continue
            elif c in [' ', '\'', '\"', ':', '[', ']', ',', '(', ')', '-']: 
                continue
            invalid = True
            break

        if invalid:
            message = "could not load message"
    return render_template('home.html', message=message) 

if __name__ == '__main__':
    app.run(host='0.0.0.0')