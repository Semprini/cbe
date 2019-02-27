# This is an example script which only return WINDOWS, i.e. the on-domain default
$versionTest = cmd /c docker --version 2`>`&1
if ($versionTest -like '*not recognized*') {
	return 'WINDOWS'
} else {
	return 'DOCKER'
} 