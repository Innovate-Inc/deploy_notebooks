def buildNumber = env.BUILD_NUMBER as int
if (buildNumber > 1) milestone(buildNumber - 1)
milestone(buildNumber)

pipeline {
    agent { docker { image 'python:3.7.9' } }

    stages {
        stage('usernamePassword') {
          steps {
            script {
              withCredentials([
                usernamePassword(credentialsId: 'agol_geoplatform',
                  usernameVariable: 'username',
                  passwordVariable: 'password')
              ]) {
                print 'username=' + username + 'password=' + password

                print 'username.collect { it }=' + username.collect { it }
                print 'password.collect { it }=' + password.collect { it }
              }
            }
          }
        }
        stage('build') {
            steps {
                echo 'my username: $env.CREDENTIALS.Username'
                sh 'python --version'
                sh '''
                python -m venv .venv
                . .venv/bin/activate
                pip install -r requirements.txt
                python update_ipynb.py agol_un=$username agol_pw=$password ipynb_file=R9_fires_notebook_TestUpdate.ipynb
                '''
            }
        }
    }
}

