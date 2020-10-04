# Developer Guidance

To create a local development environment (note: code in tripple ` is executed from within the Vagrant and Docker instances, see executeReadme.ps1)

## To run

Create a local copy

    git clone https://github.com/Semprini/cbe.git
    cd cbe

will use a default sqllite db

```
. { iwr -useb http://cdaf.io/static/app/downloads/cdaf.ps1 } | iex
.\automation\provisioning\base.ps1 'git python'

pip install -r requirements.txt
pip show django

python manage.py migrate
python manage.py createsuperuser superuser super@hero.net passw0rd
```

To run the development server
    
    python manage.py runserver

browse to http://localhost:8000/admin for the admin interface
browse to http://localhost:8000/api for the api interface

# Optional Tooling

    ~\automation\provisioning\base.ps1 'googlechrome' -checksum ignore
    ~\automation\provisioning\base.ps1 'git vscode'
    code --install-extension felixfbecker.php-intellisense
    code --install-extension felixfbecker.php-debug

Within VSCode install PHP and PHP Debug

# Vagrant

To create a virtual machine for development VirtualBox and Hyper-V are supported

    vagrant up

The virtual machine is accessible as build.mshome.net on Hyper-V and 172.16.17.100 on VirtualBox. From within the machine run the dev server

    cd \vagrant\var\www\tmobile_payment\
    php -S localhost:8000

# Docker

If you just want the raw runtime in a windows container

    docker build .

Volume mount your workspace into the container and port forward to the local host

   docker run --tty -p 8080:8080 --volume ${workspace}\var\www\tmobile_payment:C:/solution/workspace <container>