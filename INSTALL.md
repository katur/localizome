# Installing `localizome` Project


## Development Installation


### Get code

```
git clone https://github.com/katur/localizome.git
vi localizome/localizome/local_settings.py
# Add local_settings, setting DEBUG=True
```


### Set up dev database

Add dev database connection info to `localizome/local_settings.py`.
This might be a dev database that already exists on another machine,
or a new database on your own machine.
You might import an existing dump, or you might generate an empty database
from scratch with `./manage.py migrate`. Do whatever suits your needs.


### Python dependencies

Python version is listed in [runtime.txt](runtime.txt).

Python package dependencies, including Django,
are listed in [requirements.txt](requirements.txt).
These should be [pip](https://pypi.python.org/pypi/pip)-install into a fresh
[Python virtual environment](http://virtualenv.readthedocs.org/). I use
[virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/)
to make working with Python virtual environments easier.

In a nutshell (assuming pip, virtualenv, and virtualenvwrapper installed):
```
mkvirtualenv localizome
workon localizome
pip install -r requirements.txt

# To deactivate virtual environment
deactivate
```


### Running Django's built-in dev server

```
./manage.py runserver <IP address>:8000
```


### Some other notes about development

- There is no need to collect static files in development.
(When DEBUG=True, Django finds static files dynamically across the apps.)



## Production Installation

Here is a walkthrough of how I deployed this with Apache and modwsgi on Ubuntu.

This assumes that most sysadmin setup is already complete.
This sysadmin steps includes the following:

- installing Python and virtualenv
- installing Apache and modwsgi
- installing git
- installing MySQL
- creating a UNIX user for this project (named localizome)
- creating the project directory at /opt/local/localizome, owned by localizome
- creating a directory for data and backups at /volume/data1/project/localizome, owned by localizome
- creating a MySQL database (localizome)
- creating a MySQL read-write user (localizome) and a MySQL read-only user (localizome_ro)


### Import database

```
mysql -u localizome -p localizome < <sql dump filename>
```


### Automate database backups

```
mkdir /volume/data1/project/localizome/database_backups

mkdir /opt/local/localizome/secret
chmod 700 /opt/local/localizome/secret

touch /opt/local/localizome/secret/localizome.my.cnf
chmod 600 /opt/local/localizome/secret/localizome.my.cnf
vi /opt/local/localizome/secret/localizome.my.cnf
> [client]
> user = localizome_ro
> password = <password>

mkdir /opt/local/localizome/bin
chmod 775 /opt/local/localizome/bin

vi ~/.zshenv
> path=(/opt/local/localizome/bin $path)
source ~/.zshenv

touch /opt/local/localizome/bin/mysqldump_localizome
chmod 774 /opt/local/localizome/bin/mysqldump_localizome
vi /opt/local/localizome/bin/mysqldump_localizome
> #!/bin/sh
>
> /usr/bin/mysqldump --defaults-file=/opt/local/localizome/secret/localizome.my.cnf --single-transaction localizome | pbzip2 -c -p16 > /volume/data1/project/localizome/database_backups/localizome_`date +%Y-%m-%d_%H-%M-%S`.sql.bz2

crontab -e
> 0 4 * * 7 /opt/local/localizome/bin/mysqldump_localizome
```


### Get code

```
cd /opt/local/localizome
git clone https://github.com/katur/localizome.git

cd /opt/local/localizome/localizome/localizome
# create local_settings.py with database connection info, setting DEBUG=False
```


### Virtual environment and dependencies

```
cd /opt/local/localizome
virtualenv --python=/usr/bin/python2.7 localizomevirtualenv
# NOTE: This use of virtualenv hardcodes the name and location of the virtualenv dir.
# But the --relocatable arg has problems and is to be deprecated.
# So, to move or rename it, delete and recreate the virtualenv dir.

source /opt/local/localizome/localizomevirtualenv/bin/activate
pip install -r /opt/local/localizome/localizome/requirements.txt
```


### Collecting static files

```
source /opt/local/localizome/localizomevirtualenv/bin/activate
cd /opt/local/localizome/localizome
./manage.py collectstatic
```


### Apache configuration

```
mkdir /opt/local/localizome/apache2

vi /opt/local/localizome/apache2/localizome.conf
# Add project-specific apache settings.
# Note that part of this configuration involves serving static files directly.
# Please see the above file, on pyxis, for details.

sudo ln -s /opt/local/localizome/apache2/localizome.conf /etc/apache2/sites-enabled/003-localizome.conf

sudo vi /etc/apache2/ports.conf
# Enable/add line to Listen 80
```


### Apache commands
```
sudo service apache2 restart
sudo service apache2 start
sudo service apache2 stop
```


### Deploying changes

#### *As project user...*
```
# Dump database and record the currently-deployed git commit,
# in case reverting is necessary

# Activate Python virtual environment
source /opt/local/localizome/localizomevirtualenv/bin/activate

# Pull changes
cd /opt/local/localizome/localizome
git pull

# If changes to requirements.txt
pip install -r requirements.txt

# If new/changed static files
./manage.py collectstatic

# If new database migrations
./manage.py migrate

# If any scripts must be run
./manage.py scriptname

# If there are unit tests
./manage.py test
```

#### *As user with sudo...*
```
sudo service apache2 restart
```

If front-end changes, inspect visually.
