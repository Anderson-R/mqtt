pipeline {
    agent any
    stages {
        stage('build') {
            steps {
                sh 'python --version'
                sh 'echo "here we go again"'
            }
        }
        stage('deploy') {
            sh 'echo "this is the deploy stage"'
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
