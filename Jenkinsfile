pipeline {
    agent any
    environment {
        TAG = "dev_env"
        VERSION = "1.1.1"
    }
    stages {
        stage('build') {
            steps {
                sh 'python --version'
                echo "Build: ${VERSION}-${TAG}"
            }
        }
        stage('deploy') {
            steps {
                echo "this is the deploy stage"
            }
        }
    }
    post {
        always {
            echo "this always runs"
        }
        success {
            echo "this only runs when the run is a success"
        }
    }
}
