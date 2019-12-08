# DOCKER-VERSION 1.2.0
FROM mcr.microsoft.com/windows/servercore:ltsc2016@sha256:a8bc031f38ad457c3a04fcf72c7773014c6960978299c3dfe3e1c4d133f35190

MAINTAINER Jules Clements

ARG proxy
ENV http_proxy=$proxy

ENV PYTHONIOINPUT=UTF-8

EXPOSE 8000

# Copy solution, provision and then build
WORKDIR solution

COPY automation/provisioning automation/provisioning
COPY requirements.txt requirements.txt
COPY .cdaf/bootstrapAgent.ps1 .cdaf/bootstrapAgent.ps1

# Provision Build Dependancies
RUN automation\provisioning\runner.bat .cdaf\bootstrapAgent.ps1

# Copy the solution (do this last to utilise cache of provisioning steps)
COPY cbe cbe
COPY start.ps1 start.ps1
COPY *.py ./

CMD automation\provisioning\runner.bat start.ps1
