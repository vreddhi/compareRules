pipeline {
  agent any
  stages {
    stage('Dev') {
      parallel {
        stage('Dev') {
          steps {
            echo 'Push Changes'
          }
        }
        stage('Push Changes') {
          steps {
            echo 'Push changes'
          }
        }
        stage('Test in Staging') {
          steps {
            echo 'Test'
          }
        }
        stage('Test in Production') {
          steps {
            echo 'Test'
          }
        }
      }
    }
    stage('QA') {
      parallel {
        stage('QA') {
          steps {
            echo 'Test'
          }
        }
        stage('Push Changes') {
          steps {
            echo 'Push Changes'
          }
        }
        stage('Test in Staging') {
          steps {
            echo 'Test in Staging'
          }
        }
        stage('Test in Production') {
          steps {
            echo 'Test in Production'
          }
        }
      }
    }
    stage('PROD') {
      parallel {
        stage('PROD') {
          steps {
            echo 'Test'
          }
        }
        stage('Push Changes') {
          steps {
            echo 'Push Changes'
          }
        }
        stage('Test in Staging') {
          steps {
            echo 'Test in Staging'
          }
        }
        stage('Test in Production') {
          steps {
            echo 'Test in Production'
          }
        }
      }
    }
    stage('DONE') {
      steps {
        echo 'Done'
      }
    }
  }
}