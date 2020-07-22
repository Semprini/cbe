$scriptName = 'bootstrap.ps1'

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

# Use the CDAF provisioning helpers
Write-Host "`n[$scriptName] ---------- start ----------`n"
if ( $env:http_proxy ) {
	Write-Host "[$scriptName] Set HTTPS proxy for Python Package Manager (PiP)`n"
	executeExpression "`$env:https_proxy = '$env:http_proxy'"
}

$env:CDAF_AUTOMATION_ROOT = ".\automation"
if ( Test-Path $env:CDAF_AUTOMATION_ROOT ) {
	Write-Host "[$scriptName] Using `$env:CDAF_AUTOMATION_ROOT = $env:CDAF_AUTOMATION_ROOT (existing)`n"
} else {
	Write-Host "[$scriptName] Install CDAF to user directory`n"
	executeExpression '[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12'
	executeExpression '(New-Object System.Net.WebClient).DownloadFile("https://codeload.github.com/cdaf/windows/zip/master", "$PWD\cdaf.zip")'
	executeExpression 'Add-Type -AssemblyName System.IO.Compression.FileSystem'
	executeExpression '[System.IO.Compression.ZipFile]::ExtractToDirectory("$PWD\cdaf.zip", "$PWD")'
	$env:CDAF_AUTOMATION_ROOT = "$env:USERPROFILE\.cdaf"
	executeExpression "Move-Item .\windows-master\automation\ $env:CDAF_AUTOMATION_ROOT"
	Write-Host "[$scriptName] Using `$env:CDAF_AUTOMATION_ROOT = $env:CDAF_AUTOMATION_ROOT (downloaded from GitHub)"
}

Write-Host "`n[$scriptName] Install Chocolately, Python and Python Package Manager (PiP)`n"
executeExpression "$env:CDAF_AUTOMATION_ROOT\provisioning\base.ps1 'python git'"

if ( Test-Path "c:\vagrant" ) {
	Write-Host "`n[$scriptName] Vagrant environment`n"
	executeExpression 'cd c:\vagrant'
	executeExpression "$env:CDAF_AUTOMATION_ROOT\provisioning\setenv.ps1 CDAF_DELIVERY VAGRANT Machine"
	executeExpression "$env:CDAF_AUTOMATION_ROOT\provisioning\setenv.ps1 CDAF_AUTOMATION_ROOT $env:CDAF_AUTOMATION_ROOT User"
	executeExpression "$env:CDAF_AUTOMATION_ROOT\provisioning\addPath.ps1 $env:CDAF_AUTOMATION_ROOT User"
}

Write-Host "`n[$scriptName] Use Python Package Manager (PiP) to install dependancies:`n"
executeExpression "cat requirements.txt"

Write-Host
executeExpression 'pip install -r requirements.txt' 

Write-Host "`n[$scriptName] ---------- stop ----------`n"
