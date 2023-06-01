from flask import Flask,render_template,url_for,request
from flask_bootstrap import Bootstrap 
import pandas as pd 
import numpy as np 

# ML Packages
from sklearn.feature_extraction.text import CountVectorizer
import joblib


app = Flask(__name__)
Bootstrap(app)


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
	df= pd.read_csv("data/bengali_names.csv")
	# Features and Labels
	df_X = df["Name"]
	df_Y = df.sex
    
    # Vectorization
	corpus = df_X
	cv = CountVectorizer()
	X = cv.fit_transform(corpus) 
	
	# Loading our ML Model
	decisiontree_model = open("models/decisiontreemodel.pkl","rb")
	clf = joblib.load(decisiontree_model)

	# Receives the input query from form
	if request.method == 'POST':
		namequery = request.form['namequery']
		data = [namequery]
		vect = cv.transform(data).toarray()
		my_prediction = clf.predict(vect)
	return render_template('results.html',prediction = my_prediction,name = namequery.upper())


if __name__ == '__main__':
	app.run(debug=True, port=33507)
