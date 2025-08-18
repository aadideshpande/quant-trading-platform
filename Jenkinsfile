pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = 'dockerhub-creds'
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {
        stage('Build All Services') {
            parallel {
                stage('Build Order Service') {
                    steps {
                        dir('services/order-service') {
                            sh 'docker build -t aadideshpande1/order-service:${IMAGE_TAG} .'
                        }
                    }
                }
                stage('Build Price Service') {
                    steps {
                        dir('services/price-service') {
                            sh 'docker build -t aadideshpande1/price-service:${IMAGE_TAG} .'
                        }
                    }
                }
                stage('Build Portfolio Service') {
                    steps {
                        dir('services/portfolio-service') {
                            sh 'docker build -t aadideshpande1/portfolio-service:${IMAGE_TAG} .'
                        }
                    }
                }
                stage('Build Dashboard UI') {
                    steps {
                        dir('services/dashboard-ui') {
                            sh 'docker build -t aadideshpande1/dashboard-ui:${IMAGE_TAG} .'
                        }
                    }
                }
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests (placeholder)'
                // Add test commands here, like pytest, npm test, etc.
            }
        }

        stage('Security Scan') {
            steps {
                echo 'Running static analysis scan (placeholder)'
                // Add scan tools like Trivy, SonarQube CLI, etc.
            }
        }

        stage('Push to DockerHub') {
            steps {
                withCredentials([usernamePassword(credentialsId: "${DOCKERHUB_CREDENTIALS}", usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin

                        docker push aadideshpande1/order-service:${IMAGE_TAG}
                        docker push aadideshpande1/price-service:${IMAGE_TAG}
                        docker push aadideshpande1/portfolio-service:${IMAGE_TAG}
                        docker push aadideshpande1/dashboard-ui:${IMAGE_TAG}
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deployment logic goes here (manual or automated)'
                // We'll handle this part after your image push is confirmed working
            }
        }
    }
}
