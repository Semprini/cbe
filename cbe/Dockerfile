# DOCKER-VERSION 1.2.0
FROM microsoft/windowsservercore

MAINTAINER Jules Clements

ENV PYTHONIOINPUT=UTF-8

# CDAF Required Labels
LABEL	cdaf.@imageName@.image.branch="@branch@" \
		cdaf.@imageName@.image.build="@branch@:@buildNumber@" \
		cdaf.@imageName@.image.project="@solution@/@project@" \
		cdaf.@imageName@.image.version="@version@"

#Install Chocolately, Python and Python Package Manager, each PowerShell session will reload the PATH from previous step
RUN @powershell -NoProfile -ExecutionPolicy unrestricted -Command "iwr https://chocolatey.org/install.ps1 -UseBasicParsing | iex" 
RUN @powershell -NoProfile -ExecutionPolicy unrestricted -Command "choco install -y python3; mkdir /solution"

COPY cbe C:/solution
COPY requirements.txt C:/solution

# Fullfil application dependencies
RUN @powershell -NoProfile -ExecutionPolicy unrestricted -Command "cd /solution ; pip install -r /tmp/requirements.txt" 

EXPOSE 8000

CMD cd /opt/@imageName@;python manage.py runserver 0.0.0.0:8000
