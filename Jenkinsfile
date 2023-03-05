timeout(time: 3, unit: 'HOURS') {
  node {

    properties(
      [
        [
          $class: 'BuildDiscarderProperty',
          strategy: [$class: 'LogRotator', numToKeepStr: '10']
        ],
          pipelineTriggers([cron('30 05 * * *')]),
      ]
    )

    try {

      stage ('Clean and get latest from GitHub') {

        checkout scm
    
        powershell '''
          Get-Content Jenkinsfile
          . { iwr -useb https://raw.githubusercontent.com/cdaf/windows/master/install.ps1 } | iex
        '''
      }

      stage ('Get latest image and Test using Docker') {
        bat '''
          SET CONTAINER_IMAGE=mcr.microsoft.com/windows/servercore:ltsc2019
          docker pull %CONTAINER_IMAGE%
          automation\\entry.bat
        '''
      }

    } catch (e) {
      
      currentBuild.result = "FAILED"
      notifyFailed()
      throw e

    } finally {

      stage ('Clean Workspace') {
        bat '''
          RMDIR /S /Q automation
        '''
      }
    }
  }
}

def notifyFailed() {

  emailext (
    recipientProviders: [[$class: 'DevelopersRecipientProvider']],
    subject: "Jenkins Job [${env.JOB_NAME}] Build [${env.BUILD_NUMBER}] failure",
    body: "Check console output at ${env.BUILD_URL}"
  )

  if (env.DEFAULT_NOTIFICATION) {
    emailext (
      to: "${env.DEFAULT_NOTIFICATION}",
      subject: "Jenkins Default Notification for [${env.JOB_NAME}] Build [${env.BUILD_NUMBER}] failure",
      body: "Check console output at ${env.BUILD_URL}"
    )
  }

}