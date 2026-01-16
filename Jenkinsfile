pipeline {
  agent any

  stages {
    stage('Checkout') {
      steps {
        git 'https://github.com/s-parkar/inventory.git'
      }
    }

    stage('Install Dependencies') {
      steps {
        sh 'pip install -r requirements.txt'
      }
    }

    stage('Run Unit Tests') {
      steps {
        sh 'pytest tests || true'
      }
    }

    stage('SonarQube Analysis') {
      steps {
        sh 'sonar-scanner'
      }
    }

    stage('Build Docker Image') {
      steps {
        sh 'docker build -t inventory-app .'
      }
    }

    stage('Deploy Application') {
      steps {
        sh '''
        docker stop inventory || true
        docker rm inventory || true
        docker run -d -p 5000:5000 --name inventory inventory-app
        '''
      }
    }
  }
}
