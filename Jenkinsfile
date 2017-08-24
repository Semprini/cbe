node {

  properties(
    [
      [
        $class: 'BuildDiscarderProperty',
        strategy: [$class: 'LogRotator', numToKeepStr: '10']
      ],
        pipelineTriggers([cron('15 07 * * *')]),
    ]
  )

  try {

    stage ('Clean and get latest from GitHub') {
      bat '''
        IF EXIST windows-master git checkout -- .
        IF EXIST windows-master git checkout master
        IF EXIST windows-master git branch -D local_branch
        IF EXIST windows-master RMDIR /S /Q windows-master
      '''

      checkout scm
  
      bat "cat Jenkinsfile"
      bat "git checkout -b local_branch"
      bat "RMDIR /S /Q automation"
      bat "curl -o windows-master.zip https://codeload.github.com/cdaf/windows/zip/master"
      bat "unzip windows-master.zip"
      bat "echo d | XCOPY %CD%\\windows-master\\automation %CD%\\automation /S /E"
      bat "cat automation/CDAF.windows | grep productVersion"
    }

    stage ('Get latest image and Test') {
      bat "docker pull microsoft/windowsservercore"
      bat "automation\\cdEmulate.bat"
    }

  } catch (e) {
    
    currentBuild.result = "FAILED"
    notifyFailed()
    throw e

  } finally {

    stage ('Discard GitHub branch') {
      bat "git checkout -- ."
      bat "git checkout master"
      bat "git branch -D local_branch"
    }
  }
}

def notifyFailed() {

  emailext (
    recipientProviders: [[$class: 'DevelopersRecipientProvider']],
    subject: "Jenkins Job [${env.JOB_NAME}] Build [${env.BUILD_NUMBER}] failure",
    body: "Check console output at ${env.BUILD_URL}"
  )
}