# -*- coding: utf-8 -*-
import numpy as np
import joblib
from flask import Flask, request, render_template,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

from dashapplication import create_dash_application

# Load ML model
model = joblib.load('heart_disease')

# Create application
app = Flask(__name__)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/FlaskHD'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'secret string'

db = SQLAlchemy(app)

create_dash_application(app)


class Heart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer, nullable=False)
    sex = db.Column(db.Integer, nullable=False)
    cp = db.Column(db.Integer, nullable=False)
    trestbps = db.Column(db.Integer, nullable=False)
    chol = db.Column(db.Integer, nullable=False)
    fbs = db.Column(db.Integer, nullable=False)
    restecg = db.Column(db.Integer, nullable=False)
    thalach = db.Column(db.Integer, nullable=False)
    exang = db.Column(db.Integer, nullable=False)
    oldpeak =db.Column(db.Float, nullable=False)
    slope =  db.Column(db.Integer, nullable=False)
    ca =  db.Column(db.Integer, nullable=False)
    thal =  db.Column(db.Integer, nullable=False)




    def __init__(self, age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal):
        self.age = age
        self.sex = sex
        self.cp = cp
        self.trestbps = trestbps
        self.chol = chol
        self.fbs = fbs
        self.restecg = restecg
        self.thalach = thalach
        self.exang = exang
        self.oldpeak = oldpeak
        self.slope = slope
        self.ca = ca
        self.thal = thal


# Bind home function to URL
@app.route('/')
def home():
    return render_template('main.html')

@app.route('/index', methods=['GET', 'POST'])
def index_func():
    if request.method == 'POST':

        return redirect(url_for('main'))
 
    return render_template('index.html')

@app.route('/learn', methods=['GET', 'POST'])
def learn():
    if request.method == 'POST':

        return redirect(url_for('main'))
    return render_template('learn.html')


# Bind predict function to URL
@app.route('/predict', methods =['POST'])
def predict():
    age = request.form["age"]
    sex = request.form["sex"]
    cp = request.form["cp"]
    trestbps = request.form["trestbps"]
    chol = request.form["chol"]
    fbs = request.form["fbs"]
    restecg = request.form["restecg"]
    thalach = request.form["thalach"]
    exang = request.form["exang"]
    oldpeak = request.form["oldpeak"]
    slope = request.form["slope"]
    ca = request.form["ca"]
    thal = request.form["thal"]
    entry = Heart(age, sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal)
    db.session.add(entry)
    db.session.commit()
    
    features = [float(i) for i in request.form.values()]
    
    array_features = [np.array(features)]
  
    prediction = model.predict(array_features)
    
    output = prediction
    
    # Check the output values and retrive the result with html tag based on the value
    if output == 1:
        return render_template('result.html', 
                               result = 'Heart disease - Unlikely. No need to worry!')
    if output == 2:
        return render_template('result.html', 
                               result = 'Heart disease - Likely.Please go and see a doctor!')

if __name__ == '__main__':
    db.create_all()
    app.run()




