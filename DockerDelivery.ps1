Param (
	[string]$buildNumber
)

$scriptName = 'DockerDelivery.ps1'
cmd /c "exit 0"

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
if ( $buildNumber ) { 
	Write-Host "[$scriptName]   buildNumber  : $buildNumber"
} else {
	# Use a simple text file (buildnumber.counter) for incrimental build number
	if ( Test-Path imagenumber.counter ) {
		$buildNumber = Get-Content imagenumber.counter
	} else {
		$buildNumber = 0
	}
	[int]$buildnumber = [convert]::ToInt32($buildNumber)
	if ( $ACTION -ne "deliveryonly" ) { # Do not incriment when just deploying
		$buildNumber += 1
	}
	Out-File imagenumber.counter -InputObject $buildNumber
	Write-Host "[$scriptName]   buildNumber  : $buildNumber (using locally generated counter)"
}

executeExpression "Copy-Item -Force dockerBuild.tsk build.tsk"
executeExpression ".\automation\processor\buildPackage.ps1 $buildNumber"

Write-Host "`n[$scriptName] ---------- stop ----------"
$error.clear()
exit 0