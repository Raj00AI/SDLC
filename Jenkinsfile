pipeline {
  agent any
  stages {
    stage('Install') {
      steps {
        bat 'python -m pip install --upgrade pip'
        bat 'pip install -r requirements.txt'
        bat 'pip install -r requirements-dev.txt'
      }
    }
    stage('Lint') {
      steps {
        bat 'ruff check .'
        bat 'black --check .'
      }
    }
    stage('Test') {
      steps {
        bat 'pytest -q'
      }
    }
  }
}
