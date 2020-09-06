# DOCKER-VERSION 1.2.0
ARG CONTAINER_IMAGE
FROM ${CONTAINER_IMAGE}

ARG proxy
ENV http_proxy=$proxy

ENV PYTHONIOINPUT=UTF-8

EXPOSE 8000

# Copy solution, provision and then build
WORKDIR C:\\solution

# Provision Build Dependancies into base image, i.e. cache
COPY .cdaf/bootstrapAgent.ps1 .
COPY cbe/requirements.txt .
RUN call powershell -NoProfile -NonInteractive -ExecutionPolicy ByPass -command ./bootstrapAgent.ps1

CMD echo Usage: docker run --tty --volume ${workspace}\:C:/solution/workspace ${imageName}:${imageTag} automation\ci.bat $buildNumber revision containerbuild
