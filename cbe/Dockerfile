# DOCKER-VERSION 1.2.0
FROM microsoft/windowsservercore

MAINTAINER Jules Clements

# CDAF Required Labels
LABEL	cdaf.@imageName@.image.branch="@branch@" \
		cdaf.@imageName@.image.build="@branch@:@buildNumber@" \
		cdaf.@imageName@.image.project="@solution@/@project@" \
		cdaf.@imageName@.image.version="@version@"

COPY requirements.txt /tmp/

# Fullfil application dependencies
RUN pip install -r /tmp/requirements.txt

# Extract and place application
ADD	@imageName@.tar.gz /opt/@imageName@

EXPOSE 8000

CMD cd /opt/@imageName@;python manage.py runserver 0.0.0.0:8000
