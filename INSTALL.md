Installing localizome Project
=============================
Here is a walkthrough of an Ubuntu deploy, using Apache
and modwsgi. WORK IN PROGRESS.


MySQL Database
--------------
```
mysql -u localizome -p localizome < <sql dump filename>
```


Code
----
```
cd /opt/local/localizome
git clone https://github.com/katur/localizome.git
cd /opt/local/localizome/localizome/localizome
# copy local_settings.py from development computer
# edit local_settings with database connection info, and set DEBUG=False
```


Virtual Environment and Dependencies
------------------------------------
```
cd /opt/local/localizome
virtualenv --python=/usr/bin/python2.7 localizomevirtualenv
# NOTE: This use of virtualenv hardcodes the name and location of the virtualenv dir.
# But the --relocatable arg has problems and is to be deprecated.
# So, to move or rename it, delete and recreate the virtualenv dir.
source localizomevirtualenv/bin/activate
pip install -r localizome/requirements.txt
```


Static Files
------------
```
# Copy static files that are excluded from git repo
cd /opt/local/localizome/localizome/website/static
rsync -avz katherine@aquarius.bio.nyu.edu:~/ka73r/projects/localizome/website/static/videos .
rsync -avz katherine@aquarius.bio.nyu.edu:~/ka73r/projects/localizome/website/static/project_wide_downloads .

source /opt/local/localizome/localizomevirtualenv/bin/activate
cd /opt/local/localizome/localizome

# Use --link to avoid copying large data/video files
./manage.py collectstatic --link
```


Running Django Built-in Development Server
------------------------------------------
```
source /opt/local/localizome/localizomevirtualenv/bin/activate
/opt/local/localizome/localizome/manage.py runserver <IP address>:8000
```


Apache Configuration
--------------------
```
cd /opt/local/localizome
mkdir apache2
cd apache2
vi localizome.conf
# add project-specific apache settings, using port 8010
sudo ln -s /opt/local/localizome/apache2/localizome.conf /etc/apache2/sites-enabled/003-localizome.conf

sudo vi /etc/apache2/ports.conf
# add line to Listen 8010
```


Apache Commands
---------------
```
sudo service apache2 restart
sudo service apache2 start
sudo service apache2 stop
```


Database Backups
----------------
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

vi ~/.profile
> PATH="/opt/local/localizome/bin:$PATH"
source ~/.profile

touch /opt/local/localizome/bin/mysqldump_localizome
chmod 774 /opt/local/localizome/bin/mysqldump_localizome
vi /opt/local/localizome/bin/mysqldump_localizome

> #!/bin/sh
>
> /usr/bin/mysqldump --defaults-file=/opt/local/localizome/secret/localizome.my.cnf --single-transaction localizome | pbzip2 -c -p16 > /volume/data1/project/localizome/database_backups/localizome_`date +%Y-%m-%d_%H-%M-%S`.sql.bz2
```


Deploying in a Nutshell -- DRAFT
--------------------------------
### As user localizome
```
# dump database, in case reverting is necessary
# record the currently-deployed git commit, in case reverting is necessary

# Activate Python virtual environment
cd /opt/local/localizome/localizome
source opt/local/localizome/localizomevirtualenv/bin/activate

# Pull changes
git pull

# If changes to requirements.txt:
pip install -r requirements.txt

# If new/changed static files:
./manage.py collectstatic --link

# If new database migrations:
./manage.py migrate

# If any scripts must be run:
./manage.py scriptname

# If there are unit tests:
./manage.py test
```

### As user with sudo
```
sudo service apache2 restart
```

If front-end changes, inspect visually.
