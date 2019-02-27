Param (
	[int]$localPort
)

$scriptName = 'nextFreePort.ps1'
cmd /c "exit 0"

# Use the CDAF provisioning helpers
Write-Host "`n[$scriptName] ---------- start ----------`n"
Write-Host "[$scriptName]   localPort : $localPort"

while ($localPort -lt 65535) {
	if (Get-NetTCPConnection | Where LocalPort -eq $localPort ) {
		$localPort += 1
	} else {
		Write-Host "[$scriptName] free port is $localPort"
		return $localPort
	}
}

Write-Host "`n[$scriptName] Failed to find a free port!"
$error.clear()
exit 1