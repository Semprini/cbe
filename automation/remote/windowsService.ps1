Param (
��[string]$serviceName,
��[string]$binpath,
  [string]$start
)
$lastExitCode = 1060
function executeRetry ($expression) {
	$wait = 10
	$retryMax = 10
	$retryCount = 0
	$exitCode = 1 # Any value other than 0 to enter the loop
	while (( $retryCount -le $retryMax ) -and ($exitCode -ne 0)) {
		$exitCode = 0
		$error.clear()
		Write-Host "[$scriptName][$retryCount] $expression"
		try {
			Invoke-Expression $expression
		    if(!$?) { Write-Host "[$scriptName] `$? = $?"; $exitCode = 1 }
		} catch { echo $_.Exception|format-list -force; $exitCode = 2 }
	    if ( $error[0] ) { Write-Host "[$scriptName] `$error[0] = $error"; $exitCode = 3 }
		if ( $LASTEXITCODE -eq 1060 ) { $LASTEXITCODE = 0 } # 3010 is a normal exit
	    if ( $LASTEXITCODE -ne 0 ) { Write-Host "[$scriptName] `$LASTEXITCODE = $LASTEXITCODE "; $exitCode = $LASTEXITCODE }
	    if ($exitCode -ne 0) {
			if ($retryCount -ge $retryMax ) {
				Write-Host "[$scriptName] Retry maximum ($retryCount) reached, exiting with code $exitCode"; exit $exitCode
			} else {
				$retryCount += 1
				Write-Host "[$scriptName] Wait $wait seconds, then retry $retryCount of $retryMax"
				sleep $wait
			}
		}
    }
}

$scriptName = 'windowsService.ps1'
Write-Host "`n[$scriptName] ---------- start ----------"
if ($serviceName) {
    Write-Host "[$scriptName] serviceName : $serviceName"
} else {
    Write-Host "[$scriptName] serviceName not passed, exit with LASTEXITCODE 564"; exit 564
}
if ($binpath) {
    Write-Host "[$scriptName] binpath     : $binpath"
	if ($start) {
	    Write-Host "[$scriptName] start       : $start"
	} else {
		$start = 'yes'
	    Write-Host "[$scriptName] start       : $start (default)"
	}
} else {
    Write-Host "[$scriptName] binpath not passed, delete service"
}

if ($binpath) {

    Write-Host "[$scriptName] sc.exe create $serviceName displayname= `"$binpath`" binpath= `"$binpath`" start= auto"
	sc.exe create $serviceName displayname= "$binpath" binpath= "$binpath" start= auto
	if ( $start -eq 'yes' ) {
		executeRetry "Start-Service $serviceName"
	} else {
	    Write-Host "[$scriptName] Start set to $start, so not attempt not executing Start-Service $serviceName"
	}
	
} else {

    Write-Host "[$scriptName] sc.exe GetDisplayName $serviceName"
	$exists = $(sc.exe GetDisplayName $serviceName)
	$exists
	if ( $exists -like '*SUCCESS*' ) { 
		executeRetry "Stop-Service $serviceName"
	    Write-Host "[$scriptName] sc.exe delete $serviceName"
		sc.exe delete $serviceName

	} else {
	
	    Write-Host "[$scriptName] $serviceName not installed, no further action required."
	}
} 

Write-Host "`n[$scriptName] ---------- stop ----------"
exit 0