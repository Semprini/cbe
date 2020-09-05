Param (
	[string]$readmePath
)

cmd /c "exit 0"
$Error.Clear()
$scriptName = 'executeReadme.ps1'

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

Write-Host "`n[$scriptName] ---------- start ----------"
if ($readmePath) {
    Write-Host "[$scriptName] readmePath : $readmePath`n"
} else {
	$readmePath = '.\readme.md'
    Write-Host "[$scriptName] readmePath : $readmePath (default)`n"
}

Write-Host "[$scriptName] hostname   : $(hostname)"
Write-Host "[$scriptName] whoami     : $(whoami)"
Write-Host "[$scriptName] pwd        : $(pwd)"

$contents = @(Get-Content $readmePath)
$execute = $False
foreach ( $line in $contents ) {
	if ( $execute ) {
		if ( $line -eq '```' ) {
			$execute = $False
		} else {
			if ( $line ) { executeExpression "$line" }
		}
	} else {
		if ( $line -eq '```' ) {
			$execute = $True
		}
	}
}

Write-Host "`n[$scriptName] ---------- stop ----------"
exit 0