Param (
	[string]$buildNumber
)

$scriptName = 'DockerDelivery.ps1'

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
				Write-Host "[$scriptName] `ndocker ps`n"
				docker ps
				Write-Host "[$scriptName] `ndocker-compose logs`n"
				docker-compose logs
				exit $exitCode
			} else {
				$retryCount += 1
				Write-Host "[$scriptName] Wait $wait seconds, then retry $retryCount of $retryMax"
				sleep $wait
			}
		}
    }
}

# Use the CDAF provisioning helpers
Write-Host "`n[$scriptName] ---------- start ----------`n"
if ( $buildNumber ) { 
	Write-Host "[$scriptName]   buildNumber : $buildNumber"
} else {
	# Use a simple text file (buildnumber.counter) for incrimental build number
	if ( Test-Path imagenumber.counter ) {
		$buildNumber = Get-Content imagenumber.counter
	} else {
		$buildNumber = 0
	}
	[int]$buildnumber = [convert]::ToInt32($buildNumber)
	if ( $ACTION -ne "deliveryonly" ) { # Do not incriment when just deploying
		$buildNumber += 1
	}
	Out-File imagenumber.counter -InputObject $buildNumber
	Write-Host "[$scriptName]   buildNumber : $buildNumber (using locally generated counter)"
}

$imageName = "cbe"
Write-Host "[$scriptName]   imageName   : $imageName"

Write-Host "`nCreate the base image, relying on docker cache to avoid unnecessary reprovisioning"
executeExpression ".\automation\remote\containerBuild.ps1 $imageName -rebuildImage imageonly"

# Retrieve the latest image number
$imageTag = 0
foreach ( $imageDetails in docker images --filter label=cdaf.${imageName}.image.version --format "{{.Tag}}" ) {
	if ($imageTag -lt [INT]$imageDetails ) { $imageTag = [INT]$imageDetails }
}

Write-Host "`nCleanup from previously failed builds`n"
executeExpression "`$env:CORE_IMAGE = '${imageName}'"
executeExpression "docker-compose down"
executeExpression "docker-compose rm"

Write-Host "Create Test Containers`n"
executeExpression "`$env:CORE_IMAGE = '${imageName}:$imageTag'"
executeExpression "docker-compose up -d"

Write-Host "Wait for migrations to start"
executeExpression "sleep 10"

Write-Host "Disable outbound proxy and test container"
$url = "http://${env:COMPUTERNAME}/admin:8000"
Write-Host "`$webClient = New-Object System.Net.WebClient"
$webClient = New-Object System.Net.WebClient
executeExpression "`$webClient.Proxy = [System.Net.GlobalProxySelection]::GetEmptyWebProxy()"
executeRetry "`$webClient.DownloadString('$url')"

Write-Host "`nTear down`n"
executeExpression "docker-compose down"
executeExpression "docker-compose rm"

Write-Host "`n[$scriptName] ---------- stop ----------"
$error.clear()
exit 0