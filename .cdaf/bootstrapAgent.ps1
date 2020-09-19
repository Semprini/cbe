Param (
	[string]$project
)

cmd /c "exit 0"
$Error.Clear()

# Common expression logging and error handling function, copied, not referenced to ensure atomic process
function executeExpression ($expression) {
	Write-Host "[$(Get-Date)] $expression"
	try {
		Invoke-Expression $expression
	    if(!$?) { Write-Host "[$scriptName] `$? = $?"; $error ; exit 1111 }
	} catch { Write-Output $_.Exception|format-list -force; $error ; exit 1112 }
    if ( $LASTEXITCODE ) {
    	if ( $LASTEXITCODE -ne 0 ) {
			Write-Host "[$scriptName] `$LASTEXITCODE = $LASTEXITCODE " -ForegroundColor Red ; $error ; exit $LASTEXITCODE
		} else {
			if ( $error ) {
				Write-Host "[$scriptName][WARN] $Error array populated by `$LASTEXITCODE = $LASTEXITCODE, $error[] = $error`n" -ForegroundColor Yellow
				$error.clear()
			}
		} 
	} else {
	    if ( $error ) {
			Write-Host "[$scriptName][WARN] $Error array populated but LASTEXITCODE not set, $error[] = $error`n" -ForegroundColor Yellow
			$error.clear()
		}
	}
}

$scriptName = 'bootstrapAgent.ps1'
Write-Host "`n[$scriptName] ---------- start ----------"
if ($project) {
    Write-Host "[$scriptName] project : $project (change to this directory)"
	executeExpression "cd $project"
} else {
    Write-Host "[$scriptName] project : (not supplied, no directory change)"
}

if ( $env:http_proxy ) {
	Write-Host "[$scriptName] Set HTTPS proxy for Python Package Manager (PiP)`n"
	executeExpression "`$env:https_proxy = '$env:http_proxy'"
}

if ( Test-Path .\automation\remote\capabilities.ps1 ) {
	$env:CDAF_AUTOMATION_ROOT = (Get-Item .\automation).FullName
	Write-Host "[$scriptName] Using `$env:CDAF_AUTOMATION_ROOT = $env:CDAF_AUTOMATION_ROOT (existing)`n"
} else {
	Write-Host "[$scriptName] Install CDAF to user directory`n"
	executeExpression "cd $env:USERPROFILE"
	executeExpression '. { iwr -useb http://cdaf.io/static/app/downloads/cdaf.ps1 } | iex'
	$env:CDAF_AUTOMATION_ROOT = "$env:USERPROFILE\automation\remote\capabilities.ps1"
}

executeExpression "$env:CDAF_AUTOMATION_ROOT\provisioning\setenv.ps1 CDAF_AUTOMATION_ROOT $env:CDAF_AUTOMATION_ROOT"
executeExpression "$env:CDAF_AUTOMATION_ROOT\provisioning\addPath.ps1 $env:CDAF_AUTOMATION_ROOT"

$versionTest = cmd /c tar --version 2`>`&1
if ( $LASTEXITCODE -ne 0 ) {
	Write-Host "`n[$scriptName] Tar not installed!`n"
	exit 6149
}
Write-Host "$versionTest"

Write-Host "`n[$scriptName] Install Chocolately, Python and Python Package Manager (PiP)`n"
executeExpression "$env:CDAF_AUTOMATION_ROOT\provisioning\base.ps1 'python git'"

Write-Host "`n[$scriptName] Use Python Package Manager (PiP) to install dependancies:`n"
executeExpression "cat requirements.txt"

Write-Host
executeExpression 'pip install -r requirements.txt' 

Write-Host "`n[$scriptName] ---------- stop ----------`n"
