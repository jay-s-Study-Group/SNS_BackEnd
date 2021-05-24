pipeline {
    agent any

    triggers {
        pollSCM('*/3 * * * *')
    }

    stages {

        stage('Prepare') {
            agent any

            steps {
                echo 'Clonning Repository'

                git url: 'https://github.com/jay-s-Study-Group/SNS_BackEnd',
                    branch : 'staging',
                    credentialsId: 'githubTokenForJenkinshanbin8269'
            }

        }

        stage('Build Image') {
            agent any
            steps {
                echo 'Build Backend Image'

                sh '''
                sudo docker build . -t ${IMAGE_NAME}
                '''
            }
        }
        
        stage('Deploy Container') {
            agent any

            steps {
                echo 'Stop and Remove existed container'
                sh '''
                docker stop ${CONTAINER_NAME} || true && docker rm ${CONTAINER_NAME} || true
                '''
                
                echo 'Run new container'
                sh '''
                sudo docker run --name ${CONTAINER_NAME} -p ${EXTERNAL_PORT}:3052 -d \
                -e SECRET_KEY=${SECRET_KEY} \
                ${IMAGE_NAME}
                '''
            }

            post {
                failure {
                    echo 'I failed'
                }
            }
        }
    }
}