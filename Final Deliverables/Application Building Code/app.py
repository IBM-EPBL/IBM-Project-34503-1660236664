from flask import Flask, render_template, request, url_for, redirect, flash
from pymongo import MongoClient
import pickle

app = Flask(__name__)

client = MongoClient('localhost', 27017, username='Rakesh', password='Rakesh@123')

db = client.flask_db
login = db.login

def ValuePredictor(to_predict_list):
	loaded_model = pickle.load(open("final_model.pkl", "rb"))
	result = loaded_model.predict(to_predict_list)
	return result[0]

@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method=='POST':
        email = request.form['email']
        uname = request.form['uname']
        password = request.form['pass']
        login.insert_one({"email": email, 'usernmae': uname, 'password': password})
        return render_template('index.html')
    
    return render_template('home.html')

@app.route('/login', methods=('GET', 'POST'))
def loginacc():
    return render_template('login.html')

@app.route('/dashboard', methods=('GET', 'POST'))
def dashboard():
    if request.method=='POST':
        coll = login.find()
        uname = request.form['uname']
        password = request.form['pass']
        print(coll, uname, password)
        for i in coll:
            if(uname==i['usernmae'] and password==i['password']):
                return render_template('dashboard.html')
    if request.method=='GET':
        return render_template('dashboard.html')

    return render_template('home.html')

@app.route('/predict', methods=('GET', 'POST'))
def predict():
    return render_template('index.html')

@app.route('/result', methods = ['POST'])
def result():
	if request.method == 'POST':
		arr = []
		name = request.form.get("pname")

		arr.append(int(request.form.get("gre")))
		arr.append(int(request.form.get("toefl")))
		arr.append(int(request.form.get("university")))
		arr.append(int(request.form.get("sop")))
		arr.append(int(request.form.get("lor")))
		arr.append(float(request.form.get("cgpa")))
		arr.append(int(request.form.get("research")))
		prediction = ValuePredictor([arr])
		print(arr,prediction)
		return render_template("chance.html", prediction=[name, round(prediction*100,2)])

if(__name__ == '__main__'):
	app.run()