Param (
	[string]$command
)

$scriptName = 'compose.ps1'

function executeWarning ($expression) {
	$error.clear()
	Write-Host "[$(date)] $expression"
	try {
		Invoke-Expression $expression
	    if(!$?) { Write-Host "[$scriptName] `$? = $?"; exit 1 }
	} catch { Write-Host $_.Exception | format-list -force; exit 2 }
    if ( $error ) { foreach ( $out in $error ) { Write-Host "[WARN][$scriptName] $out" }; $error.clear() }
    if (( $LASTEXITCODE ) -and ( $LASTEXITCODE -ne 0 )) { Write-Host "[$scriptName] `$LASTEXITCODE = $LASTEXITCODE "; exit $LASTEXITCODE }
}

cmd /c "exit 0"
Write-Host "`n[$scriptName] ---------- start ----------"
if ( $command ) {
	executeWarning "$command 2> trap.log"
} else {
	executeWarning "docker-compose down --remove-orphans 2> trap.log"
	executeWarning "docker-compose rm -f 2> trap.log"
}

Write-Host "`n[$scriptName] ---------- stop ----------"
exit 0