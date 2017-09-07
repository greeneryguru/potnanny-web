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
sudo pip install Django==1.10.8


# give www-data user permissions gpio stuff
sudo usermod -a -G gpio www-data


# download greenery app
sudo git clone https://github.com/jeffleary00/greenery.git /var/www/greenery

# copy initial database to production
sudo cp /var/www/greenery/db.sqlite3 /var/www/greenery/greenery.db


# download and install Jquery, Bootstrap, Bootstrap-Toggle


# configure web app
sudo chown -R www-data /var/www 
sudo chgrp -R www-data /var/www
if [ -f /etc/nginx/sites-available/default ]; then
   sudo mv /etc/nginx/sites-available/default /etc/nginx/sites-available/default.bak
fi
sudo cp /var/www/greenery/conf/www/nginx.default /etc/nginx/sites-available/default
if [ -f /etc/nginx/sites-enabled/default ]; then
   sudo rm /etc/nginx/sites-enabled/default
fi
sudo ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default
sudo cp /var/www/greenery/conf/www/uwsgi.ini /etc/uwsgi/apps-available/uwsgi.ini
if [ -f /etc/uwsgi/apps-enabled/uwsgi.ini ]; then
   sudo rm /etc/uwsgi/apps-enabled/uwsgi.ini
fi
sudo ln -s /etc/uwsgi/apps-available/uwsgi.ini /etc/uwsgi/apps-enabled/uwsgi.ini


# restart services
sudo service uwsgi restart
sudo service nginx restart







