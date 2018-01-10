# Pot Nanny
*"plant care when you're not there"*
Environment monitoring and automation tool for potted plants and small greenhouses. 

## Application Overview
Basic Features:
* Monitoring of temperature, humidity, and soil moisture sensors.
* Graphing and reporting of sensor data.
* Control of wireless power outlets.
    * manual on/off control.
    * daily schedules.
    * threshold based control, triggered by incoming sensor data.
* SMS message alerting based on sensor thresholds.

Pot Nanny is a responsive, mobile-first, web application that can viewed with almost any browser.

## Wireless Power Outlets
Pot Nanny can control up to 254 wireless power outlets, like the [Etekcity](https://www.amazon.com/Etekcity-Wireless-Electrical-Household-Appliances/dp/B00DQELHBS/ref=lp_5569938011_1_8/145-4080887-7927762?srs=5569938011&ie=UTF8&qid=1515171610&sr=8-8).
These outlets are less expensive, and easier to set up, than WiFi/IOT-connected smart outlets.

Most low-power appliances (LED Lights, Fans, and Humidifiers) can be plugged into the wireless outlets and controlled by Pot Nanny.

## System Details
The Pot Nanny system consists of a [Raspberry Pi](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/) running the web server and data collectors, and an [Arduino Nano](https://store.arduino.cc/usa/arduino-nano) controlling the sensors and wireless rf communication.

## Tests
Tests are found in the /tests folder. 
Run the tests with [nose2](https://github.com/nose-devs/nose2)

## Security
Pot Nanny is accessible only from within your home/local network. 
This means your information and activities are kept safely behind your network firewall, and not sent across the internet.
Additionally, users must authenticate on the system, and HTTPS is utilized to keep data encrypted across the network.

## Internet Access
It is possible to allow outside access from the internet by using [PiTunnel](https://www.pitunnel.com).

## Software
Pot Nanny uses the following open-source software.
* [Python 3](https://www.python.org/download/releases/3.0/)
* [Flask](http://flask.pocoo.org)
* [Sqlalchemy](https://github.com/zzzeek/sqlalchemy)
* [SQLite](https://www.sqlite.org)
* [Nginx](https://www.nginx.com)
* [JQuery](https://jquery.com)
* [Chart.js](http://www.chartjs.org)

Support Free and Open Source Software.





