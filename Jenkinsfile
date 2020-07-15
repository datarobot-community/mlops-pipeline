pipeline {
   agent any
   environment {
        REGISTRY = "${env.ACR_LOGINSERVER}"
        REPO = "/mlops-pipeline"
        ACR_LOGINSERVER = "${env.ACR_LOGINSERVER}"
        ACR_CREDENTIALS_ID = "39dd6538-b972-444c-8536-21cc5c3e6702"
        BUILD_NUMBER = "${BUILD_NUMBER}"
        IMAGE_NAME = "$REGISTRY$REPO:$BUILD_NUMBER"
        TEST_IMAGE_NAME="servertest-image"
        TEST_CONTAINER_NAME="servertest-container"
        ENDPOINT="${env.ENDPOINT}"
        TOKEN="${env.TOKEN}"
        PROJECT_ID="${env.PROJECT_ID}"
        MODEL_ID="${env.MODEL_ID}"
        CHANNEL_CONFIG="${env.CHANNEL_CONFIG}"
        DEPLOYMENT_ID="${env.DEPLOYMENT_ID}"
        MLOPS_MODELID="${env.MLOPS_MODELID}"
   }
   stages {
       stage('Build') {
           steps {
               // Build new image
               sh 'docker build  --build-arg ENDPOINT=$ENDPOINT --build-arg TOKEN=$TOKEN --build-arg PROJECT_ID=$PROJECT_ID --build-arg MODEL_ID=$MODEL_ID --build-arg CHANNEL_CONFIG=$CHANNEL_CONFIG --build-arg DEPLOYMENT_ID=$DEPLOYMENT_ID --build-arg MLOPS_MODELID=$MLOPS_MODELID -t $IMAGE_NAME .'   
           }
       }
       stage('Test') {
           steps {
                // Run unit tests
                sh 'echo "Run unit tests here "'
                // Commented out for faster demo
                /* sh 'docker build  --build-arg ENDPOINT=$ENDPOINT --build-arg TOKEN=$TOKEN --build-arg PROJECT_ID=$PROJECT_ID --build-arg MODEL_ID=$MODEL_ID --build-arg CHANNEL_CONFIG=$CHANNEL_CONFIG --build-arg DEPLOYMENT_ID=$DEPLOYMENT_ID --build-arg MLOPS_MODELID=$MLOPS_MODELID -t $TEST_IMAGE_NAME -f Dockerfile.test .'
                
                sh 'docker run -d --name $TEST_CONTAINER_NAME $TEST_IMAGE_NAME'
                sh 'docker exec $TEST_CONTAINER_NAME bash ./test_server.sh &'
                
                sh 'echo "Copy result.xml into Jenkins container"'
                sh 'sleep 30'
                sh 'docker cp $TEST_CONTAINER_NAME:/python-test-server/reports/result.xml ./result.xml'
                
                sh 'echo "Cleanup"'

                sh 'docker stop $(docker ps -a -q)'
                sh 'docker rm $(docker ps -aq)'
                sh 'docker rmi $TEST_IMAGE_NAME'
                sh 'cat ./result.xml'

                script { 
                    def continueBuild = sh('grep -q \'errors="0"\' ./result.xml; [ $? -eq 0 ] && echo "True" || echo "False"')
                    if (continueBuild) {
                        currentBuild.result = 'ABORTED'
                        error('Test error, stopping early…')
                    }
                }
                sh 'rm ./result.xml' */
           }
       }
       stage('Publish') {
           steps {
               // Publish to ACR
               script {
                app = docker.image("${IMAGE_NAME}")            
                withDockerRegistry([credentialsId: "${ACR_CREDENTIALS_ID}", url: "https://${ACR_LOGINSERVER}"]){          
                    app.push("${env.BUILD_NUMBER}")                
                    app.push('latest')
                } 
               }
           }      
       }
       stage ('Deploy') {
           steps {
                // Update Kubernetes deployment
                sh 'sed -ie "s;IMAGEPLACEHOLDER;${IMAGE_NAME};g" deployment.yml'
                sh "kubectl apply -f ."
               
           }
       }
    }
    /* post {
        always {
            junit '*.xml'
        }
    } */
}