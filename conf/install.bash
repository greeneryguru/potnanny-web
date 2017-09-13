#!/bin/bash

#
# 
# Raspberry Pi setup script for greenery.guru enviro automation tool.
#
#

# base installs
sudo apt-get update
sudo apt-get -y install build-essential
sudo apt-get -y install python3-dev
sudo apt-get -y install python3-cryptography
sudo apt-get -y install sqlite3
sudo apt-get -y install python3-pip


# webserver
sudo apt-get -y install nginx
sudo apt-get -y install uwsgi
sudo apt-get -y install uwsgi-plugin-python3


# flask requirements
sudo pip3 install flask
sudo pip3 install flask-login
sudo pip3 install flask-wtf
sudo pip3 install flask-sqlalchemy
sudo pip3 install sqlalchemy-migrate


# download greenery app
sudo git clone https://github.com/jeffleary00/greenery.git /var/www/greenery


# configure web interface uwsgi/nginx
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


# inital app db
cd /var/www/greenery
sudo cp initial.db app.db


# restart services
sudo service uwsgi restart
sudo service nginx restart


# add pi user to www-data
sudo usermod -a -G www-data pi


# add env variables to pi
cat $HOME/.profile | grep GREENERY_WEB
catch = $?
if (( catch )); then
    echo "GREENERY_WEB=/var/www/greenery" >> $HOME/.profile
    echo "export GREENERY_WEB" >> $HOME/.profile
fi


# install base crontab file for pi
sudo ls -l /var/spool/cron/crontabs/pi
catch = $?
if (( catch )); then
    sudo touch /var/spool/cron/crontabs/pi
fi


# setup scheduler cron for pi
crontab -l | grep "$GREENERY_WEB/scheduler.py"
catch = $?
if (( catch )); then
    sudo echo "* * * * * bash -c 'source $HOME/.profile; $GREENERY_WEB/scheduler.py'" >> /var/spool/cron/crontab/pi
fi
sudo -u www-data touch /var/tmp/greenery.scheduler.log




