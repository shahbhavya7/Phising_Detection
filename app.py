#importing required libraries

from flask import Flask, request, render_template
import numpy as np
import pandas as pd
from sklearn import metrics 
import warnings
import pickle
warnings.filterwarnings('ignore')
from feature import FeatureExtraction # this class is specially created to extract features from the url using beautiful soup and other libraries

file = open("pickle/model.pkl","rb") #load the model from pickle file
gbc = pickle.load(file)
file.close()


app = Flask(__name__) #creating flask app instance

@app.route("/", methods=["GET", "POST"]) #creating route for home page , it will accept both GET and POST requests
def index(): # defining index function for home page which will be called when user hits the home page
    # if the request method is POST, it means user has submitted the form
    if request.method == "POST": # if the request method is POST 

        url = request.form["url"] # get the url from the form
        obj = FeatureExtraction(url) # create an object of FeatureExtraction class and pass the url to it
        x = np.array(obj.getFeaturesList()).reshape(1,30) # obj returns a list of features, we convert it to numpy array and reshape it to 1 row and 30 columns

        y_pred =gbc.predict(x)[0] # predict the class of the url using the model
        #1 is safe       
        #-1 is unsafe
        y_pro_phishing = gbc.predict_proba(x)[0,0] # get the probability of the url being phishing 
        y_pro_non_phishing = gbc.predict_proba(x)[0,1] # get the probability of the url being non phishing
        # if(y_pred ==1 ): 
        pred = "It is {0:.2f} % safe to go ".format(y_pro_phishing*100) # if the url is safe, display the probability of it being safe , this is not rendered in the template
        return render_template('index.html',xx =round(y_pro_non_phishing,2),url=url ) # render the index.html template and pass the prediction and url to it
    return render_template("index.html", xx =-1) # if the request method is GET, render the index.html template with default values


if __name__ == "__main__":
    app.run(debug=True)