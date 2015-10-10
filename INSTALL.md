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
source /opt/local/localizome/localizomevirtualenv/bin/activate
cd /opt/local/localizome/localizome
./manage.py collectstatic
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
cd /etc/apache2
vi ports.conf
# add line to Listen 8010
```

Apache Commands
---------------
```
sudo service apache2 restart
sudo service apache2 start
sudo service apache2 stop
```

Deploying (to be fleshed out and automated)
-------------------------------------------
```
### As user localizome...
# dump database, in case reverting is necessary
# record the currently-deployed git commit, in case reverting is necessary
cd /opt/local/localizome/localizome
source opt/local/localizome/localizomevirtualenv/bin/activate
git pull
# if requirements.txt changed:
pip install -r requirements.txt
# if new database migrations:
./manage.py migrate
# if any scripts must be run, e.g. to modify data in keeping with schema changes:
./manage.py scriptname
# if unit tests:
./manage.py test

### As user katherine...
sudo service apache2 restart
# if front-end changes, visual inspection of site
# if necessary, revert the repo, db, and packages to the recorded versions.
```
