# DOCKER-VERSION 1.2.0
FROM mcr.microsoft.com/windows/servercore:ltsc2016@sha256:5bd97dbab1afe8d3200f5d5c974df3b0130e74e8a69fddcd427699c4c8cb5037

ARG proxy
ENV http_proxy=$proxy

ENV PYTHONIOINPUT=UTF-8

EXPOSE 8000

# Copy solution, provision and then build
WORKDIR C:\\solution

COPY automation/provisioning automation/provisioning
COPY requirements.txt requirements.txt
COPY .cdaf/bootstrap.ps1 .cdaf/bootstrap.ps1

COPY cbe cbe
WORKDIR C:\\solution\\cbe

# Provision Build Dependancies
RUN ..\automation\provisioning\runner.bat .cdaf\bootstrap.ps1

CMD ..\automation\provisioning\runner.bat start.ps1
