# DOCKER-VERSION 1.2.0
ARG CONTAINER_IMAGE
FROM ${CONTAINER_IMAGE}

# Create root, i.e. C:\solution
WORKDIR /solution

# Copy entire directory (rely on storeForLocal to limit to only to required, unlike containerBuild)
COPY automation automation

COPY bootstrapPython.ps1 .
RUN automation\provisioning\runner.bat bootstrapPython.ps1

# Install runtime dependencies at System Level
RUN RMDIR /Q/S C:\python37\lib\site-packages
COPY site-packages /python37/lib/site-packages

# Install the application
COPY cbe cbe
COPY templates templates

COPY manage.py .
RUN python manage.py migrate
RUN python manage.py createsuperuser superuser super@hero.net passw0rd

ARG GITHUB_RUN_NUMBER
ENV GITHUB_RUN_NUMBER=$GITHUB_RUN_NUMBER

CMD "python -u manage.py runserver 0.0.0.0:8000"