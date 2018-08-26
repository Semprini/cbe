Param (
	[string]$SOLUTION,
	[string]$BUILDNUMBER,
	[string]$REVISION,
	[string]$PROJECT,
	[string]$ENVIRONMENT,
	[string]$ACTION
)

$scriptName = 'build.ps1'

# Common expression logging and error handling function, copied, not referenced to ensure atomic process
function executeExpression ($expression) {
	$error.clear()
	Write-Host "[$scriptName] $expression"
	try {
		Invoke-Expression $expression
	    if(!$?) { Write-Host "[$scriptName] `$? = $?"; exit 1 }
	} catch { echo $_.Exception|format-list -force; exit 2 }
    if ( $error[0] ) { Write-Host "[$scriptName] `$error[0] = $error"; exit 3 }
    if (( $LASTEXITCODE ) -and ( $LASTEXITCODE -ne 0 )) { Write-Host "[$scriptName] `$LASTEXITCODE = $LASTEXITCODE "; exit $LASTEXITCODE }
}

function executeRetry ($expression) {
	$exitCode = 1
	$wait = 10
	$retryMax = 5
	$retryCount = 0
	while (( $retryCount -le $retryMax ) -and ($exitCode -ne 0)) {
		$exitCode = 0
		$error.clear()
		Write-Host "[$scriptName][$retryCount] $expression"
		try {
			Invoke-Expression $expression
		    if(!$?) { Write-Host "[$scriptName] `$? = $?"; $exitCode = 1 }
		} catch { Write-Host "[$scriptName] $_"; $exitCode = 2 }
	    if ( $error[0] ) { Write-Host "[$scriptName] Warning, message in `$error[0] = $error"; $error.clear() } # do not treat messages in error array as failure
	    if (( $LASTEXITCODE ) -and ( $LASTEXITCODE -ne 0 )) { Write-Host "[$scriptName] `$lastExitCode = $lastExitCode "; $exitCode = $LASTEXITCODE }
	    if ($exitCode -ne 0) {
			if ($retryCount -ge $retryMax ) {
				Write-Host "[$scriptName] Retry maximum ($retryCount) reached, listing docker images and processes for diagnostics and exiting with `$LASTEXITCODE = $exitCode.`n"
				Write-Host "[$scriptName] docker images`n"
				docker images
				Write-Host "`n[$scriptName] docker ps`n"
				docker ps
				Write-Host "`n[$scriptName] docker-compose logs`n"
				docker-compose logs
				exit $exitCode
			} else {
				$retryCount += 1
				Write-Host "[$scriptName] Wait $wait seconds, then retry $retryCount of $retryMax"
				Write-Host "[$scriptName] docker-compose logs`n"
				docker-compose logs
				sleep $wait
			}
		}
    }
}

# Replace in file
#  required : file, relative to current workspace
#  required : name, the token to be replaced
#  required : value, the replacement value
function REPLAC( $fileName, $token, $value )
{
	try {
	(Get-Content $fileName | ForEach-Object { $_ -replace [regex]::Escape($token), "$value" } ) | Set-Content $fileName
	    if(!$?) { taskException "REPLAC_TRAP" }
	} catch { taskException "REPLAC_TRAP" $_ }
}

# Use the CDAF provisioning helpers
Write-Host "`n[$scriptName] ---------- start ----------`n"
Write-Host "[$scriptName]   SOLUTION    : $SOLUTION"
Write-Host "[$scriptName]   BUILDNUMBER : $BUILDNUMBER"
Write-Host "[$scriptName]   REVISION    : $REVISION"
Write-Host "[$scriptName]   PROJECT     : $PROJECT"
Write-Host "[$scriptName]   ENVIRONMENT : $ENVIRONMENT"
Write-Host "[$scriptName]   ACTION      : $ACTION"

$versionTest = cmd /c docker --version 2`>`&1
cmd /c "exit 0"
if ($versionTest -like '*not recognized*') {
	Write-Host "[$scriptName]   Docker      : not installed"
	Write-Host "`n[$scriptName] Docker not installed so no build activity required."
} else {
	$array = $versionTest.split(" ")
	Write-Host "[$scriptName]   Docker      : $($array[2])"

#	Write-Host "`nDisable debug"
#	REPLAC cbe/settings.py 'DEBUG = True' 'DEBUG = False'
#	cat cbe/settings.py | findstr /C:"DEBUG ="
	
	Write-Host "`n[$scriptName] Create the base image, relying on docker cache to avoid unnecessary reprovisioning"
	cat Dockerfile
	
	executeExpression "automation/remote/dockerBuild.ps1 $SOLUTION $BUILDNUMBER"
	
#	Write-Host "`nRe-enable debug"
#	REPLAC cbe/settings.py 'DEBUG = False' 'DEBUG = True'
#	cat cbe/settings.py | findstr /C:"DEBUG ="
	
	Write-Host "`n[$scriptName] Cleanup any previously failed smoke test`n"
	executeExpression "`$env:CORE_IMAGE = '${SOLUTION}'"
	executeExpression 'docker-compose down --remove-orphans'
	executeExpression 'docker-compose rm'
	
	Write-Host "[$scriptName] Create Test Containers`n"
	executeExpression "`$env:CORE_IMAGE = '${SOLUTION}:$BUILDNUMBER'"
	executeExpression 'docker-compose up -d'

	executeExpression './automation/remote/dockerLog.ps1 DOCKER-COMPOSE runserver 300' # wait up to 5 minutes for migrations

	Write-Host "[$scriptName] Use shared test script, setting published port to that in the docker-compose.yml`n"
	$publishedPort = 8001
	executeExpression ".\automation-solution\customLocal\test.ps1 $publishedPort"

	Write-Host "`n[$scriptName] Tear down`n"
	executeExpression 'docker-compose down'
	executeExpression 'docker-compose rm'
}

Write-Host "`n[$scriptName] ---------- stop ----------"
$error.clear()
exit 0