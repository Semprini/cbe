$scriptName = 'start.ps1'

# Common expression logging and error handling function, copied, not referenced to ensure atomic process
function executeExpression ($expression) {
	$error.clear()
	Write-Host "[$scriptName] $expression"
	try {
		Invoke-Expression $expression
	    if(!$?) { Write-Host "[$scriptName][CDAF_DELIVERY_FAILURE.FAILURE] `$? = $?"; exit 1 }
	} catch { Write-Host "[$scriptName][CDAF_DELIVERY_FAILURE.EXCEPTION] Details follow ..." ; echo $_.Exception|format-list -force; exit 2 }
    if ( $error[0] ) { Write-Host "[$scriptName][CDAF_DELIVERY_FAILURE.ERROR] `$error[0] = $error"; exit 3 }
    if (( $LASTEXITCODE ) -and ( $LASTEXITCODE -ne 0 )) { Write-Host "[$scriptName][CDAF_DELIVERY_FAILURE.EXIT] `$LASTEXITCODE = $LASTEXITCODE "; exit $LASTEXITCODE }
}

Write-Host "`n[$scriptName] ---------- start ----------`n"

executeExpression "python manage.py migrate"
executeExpression "python deploy.py"
executeExpression "python manage.py runserver 0.0.0.0:8000"

Write-Host "`n[$scriptName] ---------- stop ----------"
$error.clear()
exit 0
