#!/bin/bash
apt-get update
apt-get install python3-pip -y
pip3 install virtualenv
cd /home/ubuntu
git clone https://github.com/thejungwon/aws-sample-general-app
cd aws-sample-general-app
virtualenv venv
. venv/bin/activate
pip3 install -r requirements.txt
cp main.service /etc/systemd
systemctl start main
systemctl enable main
