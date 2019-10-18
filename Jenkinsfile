pipeline {
    agent none 
    options {
        skipStagesAfterUnstable()
    }
    stages {
        stage('Build') { 
            agent {
                docker {
                    image 'python:3.7.4-alpine' 
                }
            }
            steps {
                sh 'python -m py_compile ppa2src.py' 
            }
        }
         stage('Test') {
            agent {
                docker {
                    image 'qnib/pytest'
                }
            }
            steps {
                sh 'py.test -v ppa2_test.py'
            }
        }
    }
}