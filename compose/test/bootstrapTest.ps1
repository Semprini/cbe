cmd /c "exit 0"
$Error.Clear()
$scriptName = 'bootstrapTest.ps1'

# Common expression logging and error handling function, copied, not referenced to ensure atomic process
function executeExpression ($expression) {
	Write-Host "[$(Get-Date)] $expression"
	try {
		Invoke-Expression "$expression 2> `$null"
	    if(!$?) {
			Write-Host "[$scriptName] `$? = $?"
			if ( $error ) { Write-Host "[$scriptName][STATUS] `$Error = $Error" ; $Error.clear() }
			exit 1111
		}
	} catch {
		Write-Host "[$scriptName][EXCEPTION] List exception and error array (if populated) and exit with LASTEXITCIDE 1112" -ForegroundColor Red
		Write-Host $_.Exception|format-list -force
		if ( $error ) { Write-Host "[$scriptName] `$Error = $Error" ; $Error.clear() }
		exit 1112
	}
    if ( $LASTEXITCODE ) {
    	if ( $LASTEXITCODE -ne 0 ) {
			Write-Host "[$scriptName][EXIT] `$LASTEXITCODE = $LASTEXITCODE " -ForegroundColor Red
			if ( $error ) { Write-Host "[$scriptName] `$Error = $Error" ; $Error.clear() }
			exit $LASTEXITCODE
		} else {
			if ( $error ) {
				Write-Host "[$scriptName][WARN] $Error array populated by `$LASTEXITCODE = $LASTEXITCODE error follows...`n" -ForegroundColor Yellow
				Write-Host "[$scriptName] `$Error = $Error" ; $Error.clear()
			}
		} 
	} else {
	    if ( $error ) {
	    	if ( $env:CDAF_IGNORE_WARNING -eq 'no' ) {
				Write-Host "[$scriptName][ERROR] `$Error = $error"; $Error.clear()
				Write-Host "[$scriptName] `$env:CDAF_IGNORE_WARNING is 'no' so exiting with LASTEXITCODE 1113 ..."; exit 1113
	    	} else {
		    	Write-Host "[$scriptName][WARN] `$Error = $error" ; $Error.clear()
	    	}
		}
	}
}

Write-Host "`n[$scriptName] ---------- start ----------`n"
$workspace = Get-Location
Write-Host "[$scriptName] pwd     : $workspace"

if ( $env:http_proxy ) {
	Write-Host "[$scriptName] Set HTTPS proxy for Python Package Manager (PiP)`n"
	executeExpression "`$env:https_proxy = '$env:http_proxy'"
}

if ( Test-Path .\automation\remote\capabilities.ps1 ) {
	$env:CDAF_AUTOMATION_ROOT = (Get-Item .\automation).FullName
	Write-Host "[$scriptName] Found .\automation\remote\capabilities.ps1, set `$env:CDAF_AUTOMATION_ROOT = $env:CDAF_AUTOMATION_ROOT`n"
} else {
	Write-Host "[$scriptName] Install CDAF to user directory`n"
	executeExpression "cd $env:USERPROFILE"
	executeExpression '. { iwr -useb http://cdaf.io/static/app/downloads/cdaf.ps1 } | iex'
	$env:CDAF_AUTOMATION_ROOT = "$env:USERPROFILE\automation"
	Write-Host "[$scriptName] Installed CDAF, set `$env:CDAF_AUTOMATION_ROOT = $env:CDAF_AUTOMATION_ROOT`n"
	executeExpression "cd $workspace"
}

executeExpression "$env:CDAF_AUTOMATION_ROOT\provisioning\setenv.ps1 CDAF_AUTOMATION_ROOT $env:CDAF_AUTOMATION_ROOT"
executeExpression "$env:CDAF_AUTOMATION_ROOT\provisioning\addPath.ps1 $env:CDAF_AUTOMATION_ROOT"
executeExpression "$env:CDAF_AUTOMATION_ROOT\provisioning\addPath.ps1 $env:CDAF_AUTOMATION_ROOT\provisioning"

Write-Host "[$scriptName] List installed components`n"
executeExpression "$env:CDAF_AUTOMATION_ROOT\remote\capabilities.ps1"

Write-Host "`n[$scriptName] ---------- stop ----------"
