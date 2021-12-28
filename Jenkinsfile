def buildNumber = env.BUILD_NUMBER as int
if (buildNumber > 1) milestone(buildNumber - 1)
milestone(buildNumber)

pipeline {
    agent { docker { image 'python:3.7.9' } }
    environment {
        CREDENTIALS = credentials('agol_geoplatform')
        echo 'agol username: $CREDENTIALS.Username'
        }

    stages {
        stage('build') {
            steps {
                sh 'python --version'
                sh '''
                python -m venv .venv
                . .venv/bin/activate
                pip install -r requirements.txt
                python update_ipynb.py agol_un=testusername agol_pw=testpw ipynb_file=R9_fires_notebook_TestUpdate.ipynb
                '''
            }
        }
    }
}

