# Import all your necessary packages
import requests
import sys
import pprint
import pandas as pd
from pandas.io.json import json_normalize
from datetime import date
import datetime 
import time
import random
import datarobot as dr
import json
import subprocess
from datarobot.mlops.mlops import MLOps
import time
import os
import numpy as np
import argparse
import math
import json


# read config
"""App configuration."""
from os import environ, path
from dotenv import load_dotenv

# Find .env file
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

HOST = environ.get('DATAROBOT_ENDPOINT')
API_TOKEN = environ.get('DATAROBOT_API_TOKEN')
CHANNEL_CONFIG = environ.get('CHANNEL_CONFIG')
PROJECT_ID = environ.get('PROJECT_ID')
MODEL_ID = environ.get('MODEL_ID')
MLOPS_MODELID = environ.get('MLOPS_MODELID')
DEPLOYMENT_ID = environ.get('DEPLOYMENT_ID')



# flippers to customize autoML model training flow
USE_AUTOPILOT = False
PRIME = False
SCORINGCODE = True
USE_EXISTING = True



drclient = dr.Client(endpoint=HOST,token=API_TOKEN)
if USE_EXISTING == False:
    # training set
    TrainingDataSet = pd.read_csv('https://s3.amazonaws.com/datarobot_public_datasets/DR_Demo_LendingClub_Guardrails.csv',nrows=1900)
    # 1. create a new project, upload data and determine best model
    if USE_AUTOPILOT == True:
        newProject = dr.Project.start(sourcedata=TrainingDataSet, project_name='Python Lending Club ' + str(date.today()) , target='is_bad', autopilot_on=True)
        newProject.set_worker_count(8)
        newProject.wait_for_autopilot()
        recommendation_type = dr.enums.RECOMMENDED_MODEL_TYPE.RECOMMENDED_FOR_DEPLOYMENT
        recommendation = dr.models.ModelRecommendation.get(newProject.id, recommendation_type)
        MODEL_ID = recommendation.model_id
        PROJECT_ID = newProject.id
        
    if USE_AUTOPILOT == False:
        newProject = dr.Project.start(sourcedata=TrainingDataSet, project_name='Python Lending Club ' + str(date.today()) , target='is_bad', autopilot_on=False)
        newProject.set_worker_count(8)

        blueprints =  newProject.get_blueprints()
        for blueprint in blueprints:
            if blueprint.model_type == 'Decision Tree Classifier (Gini)':
                bestblueprint = blueprint
                break
        newProject.unlock_holdout()
        JobId = newProject.train(bestblueprint, sample_pct=100)
        newModel = dr.models.modeljob.wait_for_async_model_creation(project_id=newProject.id, model_job_id=JobId)
        fi = newModel.get_or_request_feature_impact(600)
        MODEL_ID = newModel.id
        PROJECT_ID = newProject.id

    # 2. Download model artefact for best performing model (e.g. Prime, MLOps file, or POJO (Scoring Code) as done here)
    bestmodel = dr.Model.get(model_id= MODEL_ID, project= PROJECT_ID)

    if PRIME == True:
        prime_model = dr.PrimeModel.get(model_id=MODEL_ID, project_id= PROJECT_ID)
        validation_job = prime_model.request_download_validation(dr.enums.PRIME_LANGUAGE.PYTHON)
        prime_file = validation_job.get_result_when_complete()
        if not prime_file.is_valid:
            raise ValueError('File was not valid')
        prime_file.download('./drprime.py')
        
    if SCORINGCODE == True:
        bestmodel.download_scoring_code('./'+MODEL_ID+'.jar')


pprint.pprint(PROJECT_ID)
pprint.pprint(MODEL_ID)


def predict(data):
    # MLOPS: initialize mlops library
    deployment_id=DEPLOYMENT_ID
    model_id=MLOPS_MODELID
    mlops = MLOps() \
        .set_async_reporting(False) \
        .set_deployment_id(deployment_id) \
        .set_model_id(model_id) \
        .set_channel_config(CHANNEL_CONFIG) \
        .init()
    data=pd.DataFrame(data)
    data.to_csv('./tmp/scoringinput.csv')
    # make predictions
    start_time = time.time()
    subprocess.call(['java', '-jar', MODEL_ID+'.jar', 'csv','--input=./tmp/scoringinput.csv','--output=./tmp/scoringresult.csv'])
    result=pd.read_csv('./tmp/scoringresult.csv')
    end_time = time.time()

    # MLOPS: report deployment metrics: number of predictions and execution time
    mlops.report_deployment_stats(len(result.index), math.ceil(end_time - start_time))
    columns = list(result.columns)
    arr = result.to_numpy()
    target_column_name = columns[len(columns) - 1]
    target_values = []
    prediction_threshold = 0.5
    CLASS_NAMES = ["Yes","No"]
    # Based on prediction value and the threshold assign correct label to each prediction
    for index, value in enumerate(result.to_numpy().tolist()):
        if value[0] < prediction_threshold:
            target_values.append("Yes")
        else:
            target_values.append("No")

    feature_df = data.copy()
    feature_df[target_column_name] = target_values

    # MLOPS: features and predictions and association_ids
    mlops.report_predictions_data(
        features_df=feature_df,
        predictions=result.to_numpy().tolist(),
        class_names=CLASS_NAMES
    )
    
    # query for the stats on the record
    # shutdown/clean-up agent
    mlops.shutdown()
    
    return result

# test model predict methdod with custom input
print('test run')
jdata = '[ \
  { \
    "is_bad": "Yes", \
    "member_id": "M1236516", \
    "loan_status": "Charged Off", \
    "emp_title": "Aqua Sun Lawn and Landscaping", \
    "emp_length": "5 years", \
    "home_ownership": "RENT", \
    "annual_inc": 50000, \
    "pymnt_plan": "n", \
    "desc": "", \
    "zip_code": "282xx", \
    "addr_state": "NC", \
    "dti": 7.99, \
    "delinq_2yrs": 1, \
    "earliest_cr_line": "12/1/1998", \
    "inq_last_6mths": 1, \
    "mths_since_last_delinq": 19, \
    "mths_since_last_record": "NA", \
    "open_acc": 3, \
    "pub_rec": 0, \
    "revol_util": 13.9, \
    "total_acc": 9, \
    "initial_list_status": "FALSE", \
    "collections_12_mths_ex_med": 0, \
    "mths_since_last_major_derog": "NA", \
    "revol_util_percent": "14%", \
    "policy_code": 1 \
  } \
]'

jdata = json.loads(jdata)
print (jdata)
for d in jdata:
    for key, value in d.items():
        print (key, value)
result = predict(jdata)
print('test results:\n' + str(result))