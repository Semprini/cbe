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

Write-Host "[$scriptName] Install Chocolately, Python and Python Package Manager (PiP)`n"
executeExpression "./automation/provisioning/base.ps1 'python3 git'"

Write-Host "[$scriptName] Use Python Package Manager (PiP) to install dependancies:`n"
cat requirements.txt

Write-Host
executeExpression 'pip install -r requirements.txt' 

Write-Host "`n[$scriptName] ---------- stop ----------`n"
