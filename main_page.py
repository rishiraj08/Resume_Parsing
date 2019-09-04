from flask import Flask, render_template, session, flash, redirect, url_for,Markup
from flask import request
import pandas as pd
from forms import Initial

app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'

@app.route('/', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))

    form = Initial()
    session['skills'] = form.skills.data

    return render_template('initial.html', form=form)
		
if __name__ == '__main__':
   app.run(debug = True)

