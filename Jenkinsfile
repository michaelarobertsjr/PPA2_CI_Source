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
        stage('Tests Phase using no Test Doubles') {
            agent {
                docker {
                    image 'pcp1976/pytest-3.7'
                }
            }
            steps {
                sh 'python -m pip install --upgrade pip'
                sh 'pip install sqlalchemy'
                sh 'pip install pymysql'
                sh 'pip install flask'
                sh '''pytest -v ppa2_test.py -k test_calc_functions'''
            }
        }
        stage('Tests Phase using dummy, mock Test Doubles') {
            agent {
                docker {
                    image 'pcp1976/pytest-3.7'
                }
            }
            steps {
                sh 'python -m pip install --upgrade pip'
                sh 'pip install sqlalchemy'
                sh 'pip install pymysql'
                sh 'pip install flask'
                sh '''pytest -v ppa2_test.py -k test_get_functions'''
            }
        }
    }
}