
pipeline {
    agent { docker { image 'python:3.7.9' } }
    environment {
          agol_creds = credentials('agol_geoplatform')
        //           todo - enable for list of scripts
          notebook_script = "R9_FiresNotebookDeploy.py"
    }
    stages {
        stage('checkout scm'){
            steps{
                checkout scm
            }
        }
        stage('deploy_ipynb') {
            when { changeset "**/${notebook_script}"}
                steps {
                    script {
                        withEnv(["HOME=${env.WORKSPACE}"]) {
                        sh 'python --version'
                        sh 'pip install -r requirements.txt --user'
                        sh 'python -c "import sys; print(sys.path)"'
                        // sh 'jupytext --to notebook R9_Fires.py'
                        sh('python update_ipynb.py $agol_creds_USR $agol_creds_PSW $notebook_script')
                    }
                }
            }
        }
    }
    post {
        always {

            cleanWs()
        }
    }
}

