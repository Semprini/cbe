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
        bat '''
          IF EXIST windows-master git checkout -- .
          IF EXIST windows-master git checkout master
          IF EXIST windows-master git branch -D local_branch & cmd /c "exit 0"
          IF EXIST windows-master RMDIR /S /Q windows-master
        '''

        checkout scm
    
        bat '''
          type Jenkinsfile
          git checkout -b local_branch
          RMDIR /S /Q automation
          curl -o windows-master.zip https://codeload.github.com/cdaf/windows/zip/master
          unzip windows-master.zip
          echo d | XCOPY %CD%\\windows-master\\automation %CD%\\automation /S /E
          type automation\\CDAF.windows | findstr "productVersion"
        '''
      }

      stage ('Get latest image and Test using Docker') {
        bat '''
          SET CONTAINER_IMAGE=mcr.microsoft.com/windows/servercore:ltsc2016
          automation\\entry.bat
        '''
      }

    } catch (e) {
      
      currentBuild.result = "FAILED"
      notifyFailed()
      throw e

    } finally {

      stage ('Discard GitHub branch') {
        bat '''
          git checkout -- .
          git checkout -f master
          IF EXIST windows-master git branch -D local_branch & cmd /c "exit 0"
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