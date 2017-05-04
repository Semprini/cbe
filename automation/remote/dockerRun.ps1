#!/usr/bin/env bash

function executeExpression {
	echo "[$scriptName] $1"
	eval $1
	exitCode=$?
	# Check execution normal, anything other than 0 is an exception
	if [ "$exitCode" != "0" ]; then
		echo "$0 : Exception! $EXECUTABLESCRIPT returned $exitCode"
		exit $exitCode
	fi
}  

scriptName='dockerRun.sh'
echo
echo "[$scriptName] Start a container instance, if an instance (based on \"instance\") exists it is"
echo "[$scriptName] stopped and removed before starting the new instance."
echo
echo "[$scriptName] --- start ---"
imageName=$1
if [ -z "$imageName" ]; then
	echo "[$scriptName] imageName not passed, exiting with code 1."
	exit 1
else
	echo "[$scriptName] imageName       : $imageName"
fi

dockerExpose=$2
if [ -z "$dockerExpose" ]; then
	echo "[$scriptName] dockerExpose not passed, exiting with code 2."
	exit 2
else
	echo "[$scriptName] dockerExpose    : $dockerExpose"
fi

publishedPort=$3
if [ -z "$publishedPort" ]; then
	publishedPort='80'
	echo "[$scriptName] publishedPort   : $publishedPort (default)"
else
	echo "[$scriptName] publishedPort   : $publishedPort"
fi

tag=$4
if [ -z "$tag" ]; then
	tag='latest'
	echo "[$scriptName] tag             : $tag (default)"
else
	echo "[$scriptName] tag             : $tag"
fi

environment=$5
if [ -z "$environment" ]; then
	environment=$tag
	echo "[$scriptName] environment     : $environment (not passed, set to same value as tag)"
else
	echo "[$scriptName] environment     : $environment"
fi

registry=$6
if [ -z "$registry" ]; then
	echo "[$scriptName] registry        : not passed, use local repo"
else
	if [ $registry = 'none' ]; then
		echo "[$scriptName] registry        : passed as '$registry', ignoring"
		unset registry
	else
		echo "[$scriptName] registry        : $registry"
	fi
fi

dockerOpt=$7
if [ -z "$dockerOpt" ]; then
	echo "[$scriptName] dockerOpt       : not passed"
else
	echo "[$scriptName] dockerOpt       : $dockerOpt"
fi

echo
executeExpression "docker --version"

echo
# Globally unique label, based on port, if in use, stop and remove
instance="${imageName}:${publishedPort}"
echo "[$scriptName] instance        : $instance (container ID)"

# User the 3rd party naming standard (x_y)
name="${imageName}_${publishedPort}"
echo "[$scriptName] name            : $name"

echo
echo "List the running containers (before)"
docker ps

# Test is based on combination of image name and port to force exit if the port is in use by another image 
for containerInstance in $(docker ps --filter label=cdaf.${imageName}.container.instance=${instance} -aq); do
	echo "[$scriptName] Stop and remove existing container instance ($instance)"
	executeExpression "docker stop $containerInstance"
	executeExpression "docker rm $containerInstance"
done

echo
# Labels, other than instance, are for filter purposes, only instance is important in run context. 
if [ -z "$registry" ]; then
	executeExpression "docker run -d -p ${publishedPort}:${dockerExpose} --name $name $dockerOpt --label cdaf.${imageName}.container.instance=$instance --label cdaf.${imageName}.container.environment=$environment ${imageName}:${tag}"
else
	executeExpression "docker run -d -p ${publishedPort}:${dockerExpose} --name $name $dockerOpt --label cdaf.${imageName}.container.instance=$instance --label cdaf.${imageName}.container.environment=$environment ${registry}/${imageName}:${tag}"
fi
echo
echo "List the running containers (after)"
docker ps

echo
echo "[$scriptName] --- end ---"
