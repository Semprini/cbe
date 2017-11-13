$scriptName = 'buildAgent.ps1'

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

if ( Test-Path "c:\vagrant" ) {
	executeExpression 'cd c:\vagrant'
}

Write-Host "[$scriptName] Install Chocolately, Python and Python Package Manager, each PowerShell session will reload the PATH from previous step`n"
executeExpression 'iwr https://chocolatey.org/install.ps1 -UseBasicParsing | iex'
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

executeExpression 'choco install -y python3'
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

executeExpression 'pip install -r requirements.txt' 

Write-Host "`n[$scriptName] ---------- stop ----------"
