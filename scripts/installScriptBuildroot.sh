#!/bin/bash

psplash()
{
    printf " ----- psplash  ----- \n \n "
    cp /home/Download/LinuxEmbedded/startImage/psplash /usr/bin/
}

configure_MediaServer()
{
    printf " ----- MediaServer Configuration  ----- \n\n "
    cp /home/Download/LinuxEmbedded/configFiles/*.sh /opt/
    cp /home/Download/LinuxEmbedded/configFiles/start.service /usr/lib/systemd/system/
    systemctl enable start.service
}

configure_X11()
{
    printf " ----- X11 Configuration  ----- \n\n "
    cp /home/Download/LinuxEmbedded/configFiles/x11/99-calibration.conf /usr/share/X11/xorg.conf.d/
    mv /usr/share/X11/xorg.conf.d/10-evdev.conf /usr/share/X11/xorg.conf.d/45-evdev.conf
}

configure_Ampache()
{
    #printf " ----- Ampache configuration  ----- \n\n "
    #wget https://github.com/ampache/ampache/archive/4.1.0.tar.gz
    #mkdir ampache
    #gunzip 4.1.0.tar.gz
    #tar -xf 4.1.0.tar -C ampache/
    #mkdir -p /usr/htdocs/ampache
    #mv ampache/ampache-4.1.0/* /usr/htdocs/ampache/
    #rm -rf ampache
    #rm 4.1.0.tar
       #cp /home/Download/LinuxEmbedded/website/* /usr/htdocs/
    #cp /usr/htdocs/ampache/play/.htaccess.dist /usr/htdocs/ampache/play/.htaccess
    #cp /usr/htdocs/ampache/rest/.htaccess.dist /usr/htdocs/ampache/rest/.htaccess
    #cp /usr/htdocs/ampache/channel/.htaccess.dist /usr/htdocs/ampache/channel/.htaccess
    cp /home/Download/LinuxEmbedded/configFiles/apache/httpd.conf /etc/apache2/httpd.conf
    #cp /home/Download/LinuxEmbedded/configFiles/apache/apache.service /usr/lib/systemd/system/
    #systemctl enable apache.service
    #systemctl start apache.service

    
}

set -e
#psplash
#configure_MediaServer
#configure_X11
configure_Ampache

