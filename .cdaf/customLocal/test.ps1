Param (
	[string]$testURL
)

$scriptName = 'test.ps1'
cmd /c "exit 0"

# Common expression logging and error handling function, copied, not referenced to ensure atomic process
function executeExpression ($expression) {
	$error.clear()
	Write-Host "[$scriptName] $expression"
	try {
		Invoke-Expression $expression
	    if(!$?) { Write-Host "[$scriptName] `$? = $?"; exit 1 }
	} catch { Write-Host $_.Exception|format-list -force; exit 2 }
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
				if ($docker) {
					Write-Host "[$scriptName] Retry maximum ($retryCount) reached, listing docker images and processes for diagnostics and exiting with `$LASTEXITCODE = $exitCode.`n"
					Write-Host "[$scriptName] docker images`n"
					docker images
					Write-Host "`n[$scriptName] docker ps`n"
					docker ps
					Write-Host "`n[$scriptName] docker-compose logs`n"
					docker-compose logs
				}else {
					Write-Host "[$scriptName] Retry maximum ($retryCount) reached, exiting with `$LASTEXITCODE = $exitCode.`n"
				}
				exit $exitCode
			} else {
				$retryCount += 1
				Write-Host "[$scriptName] Wait $wait seconds, then retry $retryCount of $retryMax"
				Start-Sleep $wait
			}
		}
    }
}

# Use the CDAF provisioning helpers
Write-Host "`n[$scriptName] ---------- start ----------`n"
Write-Host "[$scriptName]   testURL     : $testURL"
Write-Host "[$scriptName]   SOLUTION    : $SOLUTION"
Write-Host "[$scriptName]   BUILDNUMBER : $BUILDNUMBER"
Write-Host "[$scriptName]   ENVIRONMENT : $ENVIRONMENT"

$versionTest = cmd /c docker --version 2`>`&1
cmd /c "exit 0"
if ($versionTest -like '*not recognized*') {
	Write-Host "[$scriptName]   Docker      : not installed"
} else {
	$docker = $versionTest.split(" ")
	Write-Host "[$scriptName]   Docker      : $($docker[2])"
}

Write-Host "Disable outbound proxy and test container"
Write-Host "`$webClient = New-Object System.Net.WebClient"
$webClient = New-Object System.Net.WebClient
executeExpression "`$webClient.Proxy = [System.Net.GlobalProxySelection]::GetEmptyWebProxy()"
executeRetry "`$webClient.DownloadString('${testURL}')"
executeExpression "`$webClient.DownloadString('${testURL}/admin') | findstr /C:`"Common Business Entities`""

Write-Host "`n[$scriptName] ---------- stop ----------"
$error.clear()
exit 0