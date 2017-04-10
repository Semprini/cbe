node {

  properties(
    [
      [
        $class: 'BuildDiscarderProperty',
        strategy: [$class: 'LogRotator', numToKeepStr: '10']
      ],
        pipelineTriggers([cron('20 06 * * *')]),
    ]
  )

  try {

    stage ('Clean Previous Run') {
      bat "IF EXIST .vagrant vagrant destroy -f"
      bat "IF EXIST .vagrant vagrant box list"
      bat "IF EXIST windows-master RMDIR /S /Q windows-master"
    }
    
    stage ('Get Source and apply latest from GitHub') {
      checkout scm
  
      bat '''
        git checkout -b local_branch
        RMDIR /S /Q automation
        curl -o windows-master.zip https://codeload.github.com/cdaf/windows/zip/master
        unzip windows-master.zip
        echo d | XCOPY %CD%\\windows-master\\automation %CD%\\automation /S /E
	    cat automation/CDAF.windows | grep productVersion
	  '''
	}

    stage ('Update Image Repository, Build and Test') {
      bat 'docker pull microsoft/windowsservercore'
      bat 'automation/cdEmulate.bat'
    }
  
  } catch (e) {
    
    bat "IF EXIST .vagrant vagrant halt"
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