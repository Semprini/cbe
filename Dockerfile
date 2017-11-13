# DOCKER-VERSION 1.2.0
FROM microsoft/windowsservercore

MAINTAINER Jules Clements

ENV PYTHONIOINPUT=UTF-8

EXPOSE 8000

# Copy solution, provision and then build
WORKDIR solution

COPY automation automation
COPY requirements.txt requirements.txt
COPY automation-solution/bootstrapAgent.ps1 automation-solution/bootstrapAgent.ps1

# Provision Build Dependancies
RUN automation\provisioning\runner.bat automation-solution\bootstrapAgent.ps1

# Copy the solution (do this last to utilise cache of provisioning steps)
COPY cbe cbe
COPY start.ps1 start.ps1
COPY *.py ./

CMD automation\provisioning\runner.bat start.ps1
