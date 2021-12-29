
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
                withEnv(["HOME=${env.WORKSPACE}"]) {
                    sh 'python --version'
                    sh 'python -m venv venv'
                    sh '. venv/bin/activate'
                    sh 'pip install -r requirements.txt'
                    sh 'python -c "import sys; print(sys.path)"'
                    sh 'jupytext --to notebook R9_Fires.py'
                    sh('python update_ipynb.py $agol_creds_USR $agol_creds_PSW R9_Fires.ipynb')
                }
            }
        }
    }
}

