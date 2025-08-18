pipeline {
    agent any

    stages {
        stage('Build All Services') {
            parallel {
                stage('Build Order Service') {
                    steps {
                        dir('services/order-service') {
                            sh 'docker build -t aadideshpande1/order-service:${BUILD_NUMBER} .'
                        }
                    }
                }
                stage('Build Price Service') {
                    steps {
                        dir('services/price-service') {
                            sh 'docker build -t aadideshpande1/price-service:${BUILD_NUMBER} .'
                        }
                    }
                }
                // Add portfolio-service and dashboard-ui similarly
            }
        }
        // Add test, scan, push, deploy etc.
    }
}
