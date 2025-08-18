pipeline {
    agent any

    environment {
        DOCKER_HUB_USER = 'aadideshpande1'
        TAG = "${BUILD_NUMBER}"
    }

    stages {
        stage('Build All Services') {
            parallel {
                stage('Build Order Service') {
                    steps {
                        dir('services/order-service') {
                            sh 'docker build -t $DOCKER_HUB_USER/order-service:$TAG .'
                        }
                    }
                }
                stage('Build Price Service') {
                    steps {
                        dir('services/price-service') {
                            sh 'docker build -t $DOCKER_HUB_USER/price-service:$TAG .'
                        }
                    }
                }
                stage('Build Portfolio Service') {
                    steps {
                        dir('services/portfolio-service') {
                            sh 'docker build -t $DOCKER_HUB_USER/portfolio-service:$TAG .'
                        }
                    }
                }
                stage('Build Dashboard UI') {
                    steps {
                        dir('services/dashboard-ui') {
                            sh 'docker build -t $DOCKER_HUB_USER/dashboard-ui:$TAG .'
                        }
                    }
                }
            }
        }

        stage('Test Services') {
            parallel {
                stage('Test Python Services') {
                    steps {
                        sh 'echo "🧪 Run pytest or unit tests for Python services (if available)"'
                    }
                }
                stage('Test React UI') {
                    steps {
                        dir('services/dashboard-ui') {
                            sh 'echo "🧪 Run npm test or lint for React"'
                        }
                    }
                }
            }
        }

        stage('Security Scan') {
            steps {
                sh 'echo "🔍 Run bandit/trivy or any scanner here"'
                // Example: docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy image $DOCKER_HUB_USER/order-service:$TAG
            }
        }

        stage('Push Docker Images') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push $DOCKER_HUB_USER/order-service:$TAG
                        docker push $DOCKER_HUB_USER/price-service:$TAG
                        docker push $DOCKER_HUB_USER/portfolio-service:$TAG
                        docker push $DOCKER_HUB_USER/dashboard-ui:$TAG
                    '''
                }
            }
        }

        stage('Deploy (Placeholder)') {
            when {
                branch 'develop'
            }
            steps {
                sh 'echo "🚀 Deploy to Dev (or trigger script/kubectl apply etc.)"'
            }
        }
    }

    post {
        always {
            echo '🧹 Cleanup if needed'
        }
    }
}
