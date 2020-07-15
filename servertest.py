#!/usr/bin/env python3
from flask import Flask, request, jsonify
import json
import pickle
import pandas as pd
import numpy as np
import drmodel
import pytest
import requests

url = 'http://0.0.0.0:8000/api'
feature = [[5.8, 4.0, 1.2, 0.2]]
labels ={
  0: "setosa",
  1: "versicolor",
  2: "virginica"
}

def test_predict():
    r = requests.post(url,json={'feature': feature})
    print(labels[r.json()])
    assert labels[r.json()] == "setosa"