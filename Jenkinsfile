pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = 'dockerhub-creds'
        GIT_COMMIT_HASH = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
        IMAGE_TAG = "${BRANCH_NAME}-${BUILD_NUMBER}-${GIT_COMMIT_HASH}"
        DOCKER_REPO = 'aadideshpande1'
    }

    stages {
        stage('Build All Services') {
            parallel {
                stage('Build Order Service') {
                    steps {
                        dir('services/order-service') {
                            sh "docker build -t ${DOCKER_REPO}/quant-trading-platform-order-service:${IMAGE_TAG} ."
                        }
                    }
                }
                stage('Build Price Service') {
                    steps {
                        dir('services/price-service') {
                            sh "docker build -t ${DOCKER_REPO}/quant-trading-platform-price-service:${IMAGE_TAG} ."
                        }
                    }
                }
                stage('Build Portfolio Service') {
                    steps {
                        dir('services/portfolio-service') {
                            sh "docker build -t ${DOCKER_REPO}/quant-trading-platform-portfolio-service:${IMAGE_TAG} ."
                        }
                    }
                }
                stage('Build Dashboard UI') {
                    steps {
                        dir('services/dashboard-ui') {
                            sh "docker build -t ${DOCKER_REPO}/quant-trading-platform-dashboard-ui:${IMAGE_TAG} ."
                        }
                    }
                }
            }
        }

        stage('Test') {
            steps {
                echo '🔍 Running tests (placeholder)'
                // Add test commands like `pytest`, `npm test`, etc.
            }
        }

        stage('Security Scan') {
            steps {
                echo '🛡️ Running static analysis scan (placeholder)'
                // Add Trivy, SonarQube CLI, etc.
            }
        }

        stage('Push to DockerHub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: "${DOCKERHUB_CREDENTIALS}",
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS')]) {
                    
                    sh """
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin

                        docker push ${DOCKER_REPO}/quant-trading-platform-order-service:${IMAGE_TAG}
                        docker push ${DOCKER_REPO}/quant-trading-platform-price-service:${IMAGE_TAG}
                        docker push ${DOCKER_REPO}/quant-trading-platform-portfolio-service:${IMAGE_TAG}
                        docker push ${DOCKER_REPO}/quant-trading-platform-dashboard-ui:${IMAGE_TAG}

                        echo "Docker Image Tag: ${IMAGE_TAG}"
                    """
                }
            }
        }

        stage('Deploy') {
            when {
                expression {
                    return env.BRANCH_NAME == 'develop' || 
                        env.BRANCH_NAME.startsWith('release/') || 
                        (env.BRANCH_NAME == 'main' && currentBuild.rawBuild.getCause(hudson.model.Cause$UserIdCause) != null)
                }
            }
            steps {
                script {
                    if (env.BRANCH_NAME == 'develop') {
                        echo '✅ Auto-deploying to DEV environment...'
                        // Insert deploy-to-dev.sh or docker-compose -f docker-compose.dev.yml up -d
                    } else if (env.BRANCH_NAME.startsWith('release/')) {
                        echo '✅ Auto-deploying to STAGING environment...'
                        // Insert deploy-to-staging.sh or docker-compose -f docker-compose.staging.yml up -d
                    } else if (env.BRANCH_NAME == 'main') {
                        input message: '⚠️ Manual approval required to deploy to PROD. Proceed?', ok: 'Deploy'
                        echo '🚀 Deploying to PRODUCTION environment...'
                        // Insert deploy-to-prod.sh or docker-compose -f docker-compose.prod.yml up -d
                    }
                }
            }
        }

    }
}
