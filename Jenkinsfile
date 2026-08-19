pipeline {
    agent any

    environment {
        REGISTRY = 'ghcr.io'
        // GHCR requires lowercase namespaces. 'y0usuf' must be lowercase.
        IMAGE_NAME = 'ghcr.io/y0usuf/devsecops-cicd-assessment'
        // Immutable tag built from build number and first 7 characters of git commit SHA
        IMAGE_TAG = "build-${BUILD_NUMBER}-${GIT_COMMIT.take(7)}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Unit Test') {
            steps {
                // Run tests inside an isolated python virtual environment
                sh '''
                    python3 -m venv test_env
                    . test_env/bin/activate
                    pip install -r app/requirements.txt
                    pytest app/test_app.py
                '''
            }
        }

        stage('SAST (Semgrep)') {
            steps {
                // Scan source code for security patterns.
                sh 'semgrep scan --config auto'
            }
        }

        stage('Dependency Scan (Trivy)') {
            steps {
                // Scan application dependencies for vulnerabilities.
                // If any CRITICAL issues are found, fail the pipeline.
                sh 'trivy fs --severity CRITICAL --exit-code 1 .'
            }
        }

        stage('Docker Build') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
            }
        }

        stage('Container Scan (Trivy)') {
            steps {
                // Scan the built Docker image.
                // If any CRITICAL vulnerabilities exist, fail before pushing.
                sh "trivy image --severity CRITICAL --exit-code 1 ${IMAGE_NAME}:${IMAGE_TAG}"
            }
        }

        stage('Push Image to GHCR') {
            steps {
                // Inject GHCR Personal Access Token safely from Jenkins credentials
                withCredentials([usernamePassword(credentialsId: 'ghcr-creds', passwordVariable: 'GHCR_TOKEN', usernameVariable: 'GHCR_USER')]) {
                    sh "echo \$GHCR_TOKEN | docker login ghcr.io -u \$GHCR_USER --password-stdin"
                    sh "docker push ${IMAGE_NAME}:${IMAGE_TAG}"
                }
            }
        }

        stage('Deploy') {
            steps {
                // Safely clean up previous deployment and start the new container
                sh "docker stop my-app || true"
                sh "docker rm my-app || true"
                sh "docker run -d -p 5000:5000 --name my-app ${IMAGE_NAME}:${IMAGE_TAG}"
            }
        }

        stage('Health Check') {
            steps {
                // Wait for the server to bind to port 5000
                sleep time: 5, unit: 'SECONDS'
                // Query endpoint. Non-200 responses fail the build.
                sh "curl -f http://localhost:5000/health || exit 1"
            }
        }
    }

    post {
        always {
            // Clean up workspace and remove untagged/dangling Docker images to save space
            cleanWs()
            sh "docker image prune -f"
        }
    }
}
