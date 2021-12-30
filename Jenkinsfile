
def buildNumber = env.BUILD_NUMBER as int
if (buildNumber > 1) milestone(buildNumber - 1)
milestone(buildNumber)

pipeline {
    try {
        agent { docker { image 'python:3.7.9' } }
        environment {
              agol_creds = credentials('agol_geoplatform')
        }
        stages {
            stage('deploy_ipynb') {
                steps {
                    withEnv(["HOME=${env.WORKSPACE}"]) {
                        sh 'python --version'
                        sh 'pip install -r requirements.txt --user'
                        sh 'python -c "import sys; print(sys.path)"'
                        // sh 'jupytext --to notebook R9_Fires.py'
                        sh('python update_ipynb.py $agol_creds_USR $agol_creds_PSW R9_Fires.py')
                    }
                }
            }
        }
    } catch (Exception e) {
    echo e
//     slackSend(channel:"#r9-service-alerts", message: "Notebook deployment failed for R9-Notifications branch ${env.BRANCH_NAME}")
    } finally {
    cleanWs()
    }

}

