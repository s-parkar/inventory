pipeline {
    agent any

    environment {
        // defined in Jenkins Credentials setup
        DOCKER_CREDS = 'docker-hub-credentials' 
        IMAGE_NAME = 'your-dockerhub-username/inventory-app'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker build -t $IMAGE_NAME:latest .'
                }
            }
        }

        stage('Test') {
            steps {
                // Run a quick container to check if it starts and responds to health check
                sh 'docker run -d -p 5001:5000 --name test_app $IMAGE_NAME:latest'
                sleep 5 // wait for startup
                sh 'curl -f http://localhost:5001/health || exit 1'
                sh 'docker rm -f test_app'
            }
        }

        stage('Push to Registry') {
            // Only push if tests passed
            steps {
                script {
                    withDockerRegistry(credentialsId: DOCKER_CREDS, url: '') {
                        sh 'docker push $IMAGE_NAME:latest'
                    }
                }
            }
        }

        stage('Deploy') {
            steps {
                // Example: Restarting the docker-compose stack
                sh 'docker-compose down'
                sh 'docker-compose up -d'
            }
        }
    }
}
