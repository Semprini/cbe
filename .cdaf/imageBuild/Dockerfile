# DOCKER-VERSION 1.2.0
ARG CONTAINER_IMAGE
FROM ${CONTAINER_IMAGE}

ARG proxy
ENV http_proxy=$proxy

# Create root, i.e. C:\solution
WORKDIR /solution

# Copy entire directory (rely on storeForLocal to limit to only to required, unlike containerBuild)
COPY automation automation

COPY bootstrapPython.ps1 .
RUN automation\provisioning\runner.bat bootstrapPython.ps1

# Install runtime dependencies at System Level
RUN RMDIR /Q/S C:\python37\lib\site-packages
ADD site-packages.tar.gz /

# Install the application
ADD cbe.tar.gz .
COPY manage.py .
RUN python manage.py migrate
RUN python manage.py createsuperuser superuser super@hero.net passw0rd

CMD "python -u manage.py runserver 0.0.0.0:8000"