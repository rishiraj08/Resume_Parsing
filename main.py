from flask import Flask, render_template, session, flash, redirect, url_for,Markup
from flask import request
from forms import *
from flask_bootstrap import Bootstrap
#from Resume_Filtering_spacy_v3_updated import extract_skill_set

app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'
bootstrap = Bootstrap(app)

@app.route('/', methods=['GET','POST'])
def initial():

    form = Initial()
    if form.validate_on_submit():

        session['selection'] = form.selection.data

        if session['selection'] == 'Up/Down':
            return redirect(url_for('uploading_downloading'))
        elif session['selection'] == 'Skills':
            return redirect(url_for('skillselection'))
    
    return render_template('initial.html', form=form )



@app.route('/uploading_downloading', methods=['GET','POST'])
def uploading_downloading():

    form = up_down()
        #return redirect(url_for('final'))
    return render_template('up_down.html', form=form)


@app.route('/skillselection', methods=['GET','POST'])
def skillselection():

    form = Skills()
    if form.validate_on_submit():
        session['skills'] = form.skills.data

        print(session['skills'])

        #with open('skillset.csv','r') as Data_File:
        #    reader = csv.reader(Data_File)
        #    fields = next(reader)
        #    for row in reader:
        #        rows.append(row)
        #    all_rows = rows
        #    skillset = [val for x in all_rows for val in x]
        #session['skillset'] = stocks

        return redirect(url_for('final'))
    return render_template('skills.html',form = form)


@app.route('/final',methods=['GET','POST'])
def final():




    return render_template('final.html')


		
if __name__ == '__main__':
   app.run(debug = True)

