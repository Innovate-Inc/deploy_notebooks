def buildNumber = env.BUILD_NUMBER as int
if (buildNumber > 1) milestone(buildNumber - 1)
milestone(buildNumber)

pipeline {
    agent { docker { image 'python:3.7.9' } }
    environment {
          agol_creds = credentials('agol_geoplatform')
    }

    stages {
//         stage('usernamePassword') {
//           steps {
//             script {
//               withCredentials([
//                 usernamePassword(credentialsId: 'agol_geoplatform',
//                   usernameVariable: 'username',
//                   passwordVariable: 'password')
//               ]) {
//                 print 'username=' + username + 'password=' + password
//
//                 print 'username.collect { it }=' + username.collect { it }
//                 print 'password.collect { it }=' + password.collect { it }
//               }
//             }
//           }
//         }
        stage('build') {
            steps {
                echo 'my username $agol_creds_USR}'
                sh 'python --version'
                sh '''
                python -m venv .venv
                . .venv/bin/activate
                pip install -r requirements.txt
                python update_ipynb.py agol_un=$agol_creds_USR agol_pw=$agol_creds_PSW ipynb_file=R9_fires_notebook_TestUpdate.ipynb
                '''
            }
        }
    }
}

