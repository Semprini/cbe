Param (
  [string]$imageName,
  [string]$tag,
  [string]$rebuild
)
# Common expression logging and error handling function, copied, not referenced to ensure atomic process
function executeExpression ($expression) {
	$error.clear()
	Write-Host "[$scriptName] $expression"
	try {
		Invoke-Expression $expression
	    if(!$?) { Write-Host "[$scriptName] `$? = $?"; exit 1 }
	} catch { echo $_.Exception|format-list -force; exit 2 }
    if ( $error[0] ) { Write-Host "[$scriptName] `$error[0] = $error"; exit 3 }
    if ( $lastExitCode -ne 0 ) { Write-Host "[$scriptName] `$lastExitCode = $lastExitCode "; exit $lastExitCode }
}

$scriptName = 'dockerBuild.sh'
Write-Host "`n[$scriptName] ---------- start ----------"
Write-Host "`n[$scriptName] [$scriptName] Build docker image, resulting image naming \${imageName}"
if ($imageName) {
    Write-Host "[$scriptName] imageName : $imageName"
} else {
    Write-Host "[$scriptName] imageName not supplied, exit with `$LASTEXITCODE = 1"; exit 1
}
if ($tag) {
    Write-Host "[$scriptName] tag       : $tag"
} else {
    Write-Host "[$scriptName] tag       : not supplied"
}
if ($rebuild) {
    Write-Host "[$scriptName] rebuild   : $rebuild"
} else {
    Write-Host "[$scriptName] rebuild   : not supplied"
}

$buildCommand = 'docker build'
if ($rebuild -eq 'yes') {
	$buildCommand += " --no-cache=true"
}

if ($tag) {
	$buildCommand += " --tag ${imageName}:${tag}"
} else {
	$buildCommand += " --tag ${imageName} "
}

# Execute the constucted build command using dockerfile from current directory (.)
executeExpression "$buildCommand ."


Write-Host "`n[$scriptName] List Resulting images. Note: label is derived from Dockerfile"
executeExpression "docker images -f label=cdaf.${imageName}.image.product=${imageName}"

Write-Host "`n[$scriptName] --- end ---"
