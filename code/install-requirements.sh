#!/bin/sh
sudo apt-get -yqq update \
    && sudo apt-get -yqq dist-upgrade \
    && sudo apt-get -yqq postfix \
    && sudo apt-get -yqq install python3-pip \
    && sudo apt-get -yqq install metasploit-framework \
    && sudo apt-get -yqq install bettercap \
    && sudo pip3 install -r requirements.txt \