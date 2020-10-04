# DOCKER-VERSION 1.2.0
ARG CONTAINER_IMAGE
FROM ${CONTAINER_IMAGE}

ARG proxy
ENV http_proxy=$proxy

# Create root, i.e. C:\solution
WORKDIR /solution

# Copy entire directory (rely on storeForLocal to limit to only to required, unlike containerBuild)
COPY automation automation

# Shared bootstrap between Docker and Vagrant
COPY bootstrapPython.ps1 .
RUN automation\provisioning\runner.bat bootstrapPython.ps1

# Place entry script
COPY keepAlive.ps1 .

# Change workdir to an new (empty) folder for volume mount to work
WORKDIR /solution/workspace
ADD cbe.tar.gz .

CMD ["C:/solution/automation/provisioning/runner.bat", "../keepAlive.ps1", "TARGETLESS"]