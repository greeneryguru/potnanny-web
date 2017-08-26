#!/bin/bash

#
# 
# Raspberry Pi setup script for Greenery.guru enviro automation tool.
#
#

# base installs
sudo apt-get update
sudo apt-get -y install build-essential
sudo apt-get -y install python-dev
sudo apt-get -y install python-cryptography
sudo apt-get -y install sqlite3
sudo apt-get -y install python-pip

# webserver
sudo apt-get -y install nginx
sudo apt-get -y install uwsgi
sudo apt-get -y install uwsgi-plugin-python

# flask requirements
sudo pip install flask
sudo pip install flask-login
sudo pip install flask-mail
sudo pip install flask-wtf
sudo pip install flask-sqlalchemy
sudo pip install sqlalchemy-migrate

# download greenery app
sudo git clone https://github.com/jeffleary00/greenery.git /var/www/greenery

# build rfoutlet binary
git clone https://github.com/toofishes/rfoutlet-pi.git /tmp/rfoutlet-pi
mv /tmp/rfoutlet-pi/Makefile /tmp/rfoutlet-pi/Makefile.bak
cp /var/www/greenery/conf/rfoutlet.Makefile /tmp/rfoutlet-pi/Makefile
cd /tmp/rfoutlet-pi
sudo make
sudo -u www-data cp /tmp/rfoutlet-pi/rfoutlet /var/www/greenery/bin

# configure web app
sudo chown -R www-data /var/www 
sudo chgrp -R www-data /var/www
sudo mv /etc/nginx/sites-available/default /etc/nginx/sites-available/default.bak
sudo cp /var/www/greenery/conf/www/nginx.default /etc/nginx/sites-available/default
sudo ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default
sudo cp /var/www/greenery/conf/www/uwsgi.ini /etc/uwsgi/apps-available/uwsgi.ini
sudo ln -s /etc/uwsgi/apps-available/uwsgi.ini /etc/uwsgi/apps-enabled/uwsgi.ini

# inital app db
cd /var/www/greenery
sudo -u www-data python db_create.py

# restart services
sudo service uwsgi restart
sudo service nginx restart







