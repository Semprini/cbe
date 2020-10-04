node {

  properties(
    [
      [
        $class: 'BuildDiscarderProperty',
        strategy: [$class: 'LogRotator', numToKeepStr: '10']
      ],
        pipelineTriggers([cron('55 23 * * *')]),
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
  
      bat "type Jenkinsfile"
      bat "git checkout -b local_branch"
      bat "IF EXIST automation RMDIR /S /Q automation"
      bat "curl -o windows-master.zip https://codeload.github.com/cdaf/windows/zip/master"
      bat "unzip windows-master.zip"
      bat "echo d | XCOPY %CD%\\windows-master\\automation %CD%\\automation /S /E"
      bat 'type automation\\CDAF.windows | findstr "productVersion"'
    }

    stage ('Get latest image and Test using Docker') {
      bat "automation\\entry.bat"
    }

    stage ('Test Using Vagrant') {
      bat '''
        type Vagrantfile
        vagrant destroy -f & verify >nul
        vagrant box list & verify >nul
        vagrant up
      '''
    }

    stage ('Test Using Vagrant') {
      bat '''
        cd cbe
        type Vagrantfile
        vagrant destroy -f & verify >nul
        vagrant box list & verify >nul
        vagrant up
      '''
    }

  } catch (e) {
    
    currentBuild.result = "FAILED"
    notifyFailed()
    throw e

  } finally {

    stage ('Discard GitHub branch') {
      bat '''
        vagrant destroy -f & verify >nul
        cd cbe
        vagrant destroy -f & verify >nul
        git checkout -- .
        git checkout -f master
        git branch -D local_branch
      '''
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