from flask import Flask, request, jsonify
import json
import pickle
import pandas as pd
import numpy as np
import drmodel

app = Flask(__name__)

# Load the model
model = pickle.load(open('model.pkl','rb'))
labels ={
  0: "versicolor",   
  1: "setosa",
  2: "virginica"
}


@app.route('/api',methods=['POST'])
def predict():
	data = request.get_json(force=True)
	predict = model.predict(data['feature'])
	return jsonify(predict[0].tolist())

@app.route('/drapi',methods=['POST'])
def drpredict():
  data = request.get_json(force=True)
  prediction = drmodel.predict(data)
  return prediction.to_json()

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0', port='8000')