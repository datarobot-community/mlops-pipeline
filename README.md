**Please note:** The code in these repos is sourced from the DataRobot user community and is not owned or maintained by DataRobot, Inc. You may need to make edits or updates for this code to function properly in your environment.

# DataRobot MLOps Jenkins Pipeline Example

This is a simple example of a CI/CD pipeline with Jenkins and DataRobot MLOps.
It contains a Flask app, with two routes:
1) /api uses a simple sklearn model for scoring without MLOps
2) /drapi uses DataRobot's Scoring Code for scoring and includes MLOps for monitoring

# Instructions
1. For local tests you can first create a file '.env' that contains the below environment variables:
   
      DATAROBOT_ENDPOINT='YOUR DR ENDPOINT' \
      DATAROBOT_API_TOKEN='YOUR DR API TOKEN' \
      PROJECT_ID='YOUR DEFAULT PROJECT_ID' \
      MODEL_ID='YOUR DEFAULT MODEL_ID' \
      CHANNEL_CONFIG='YOUR MLOPS CHANNEL CONFIG' \
      DEPLOYMENT_ID='YOUR MLOPS DEPLOYMENT_ID' \
      MLOPS_MODELID='YOUR MLOPS MODEL ID' \

   Then you can create a docker image and container with the below command:
      docker build -t server-image . && docker run --env-file=.env -p 8000:8000 --name mlmodelapiserver server-image

   Alternatively you can set these environment variables, and then run:
      docker build \
      --build-arg DATAROBOT_ENDPOINT=$ENDPOINT \
      --build-arg DATAROBOT_API_TOKEN=$TOKEN \
      --build-arg PROJECT_ID=$PROJECT_ID \
      --build-arg MODEL_ID=$MODEL_ID \
      --build-arg CHANNEL_CONFIG=$CHANNEL_CONFIG \
      --build-arg DEPLOYMENT_ID=$DEPLOYMENT_ID \
      --build-arg MLOPS_MODELID=$MLOPS_MODELID \
      -t server-image . && \
      docker run -p 8000:8000 --name mlmodelapiserver server-image

   This exposes a simple REST API on http://127.0.0.1:8000 with two endpoints.
   You can use the postman collection (CICD.postman_collection.json) for testing.

2. To trigger the previously defined Jenkins pipeline, add a corresponding webhook to your repo.
   Then simply make a change, commit, and push it to the repo with the command shown below.
      git add . && git commit -m "demo trigger Jenkins CI/CD pipeline" && git push
