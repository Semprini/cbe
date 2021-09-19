# DOCKER-VERSION 1.2.0
ARG CONTAINER_IMAGE
FROM ${CONTAINER_IMAGE}

ENV PYTHONIOINPUT=UTF-8

EXPOSE 8000

# Copy solution, provision and then build
WORKDIR C:\\solution

# Provision Build Dependancies into base image, i.e. cache
COPY cbe/requirements.txt .
COPY .cdaf/bootstrapAgent.ps1 .
RUN call powershell -NoProfile -NonInteractive -ExecutionPolicy ByPass -command ./bootstrapAgent.ps1

# Change workdir to the mapped folder so that the build artefacts are available on the host
WORKDIR C:\\solution\\workspace

ARG GITHUB_RUN_NUMBER
ENV GITHUB_RUN_NUMBER=$GITHUB_RUN_NUMBER

CMD echo Usage: docker run --tty --volume ${workspace}\:C:/solution/workspace ${imageName}:${imageTag} automation\ci.bat $buildNumber revision containerbuild
