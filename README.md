# aws-sample-general-app
 
## Instruction
1. Launch one **EC2** instance (free tier, e.g., t2.micro), using the following `user data` command, and open 80 port from the `security group`.
```
#!/bin/bash
sudo apt-get update
sudo apt-get install python3-pip -y
sudo pip3 install virtualenv 
cd /home/ubuntu
git clone https://github.com/thejungwon/aws-sample-general-app
cd aws-sample-general-app
virtualenv venv
. venv/bin/activate
pip3 install -r requirements.txt
sudo apt-get  install awscli -y
python main.py
```
2. Check if the website works through the public IP address.
3. Launch one **RDS** instance (mysql, t2.micro), and open 3306 port to (only) the security group used for EC2 instance (e.g., sg.xxx)
4. Make an **S3** bucket and make it public.
5. Set up the IAM role to EC2 with full S3 access.
6. Submit the RDS and S3 information on the website that we launched.
7. Check if posting function works.
8. Launch another EC2 instance with the following command (mind the bucket name).
```
#!/bin/bash
sudo apt-get update
sudo apt-get install python3-pip -y
sudo pip3 install virtualenv 
cd /home/ubuntu
git clone https://github.com/thejungwon/aws-sample-general-app
cd aws-sample-general-app
virtualenv venv
. venv/bin/activate
pip3 install -r requirements.txt
sudo apt-get  install awscli -y
aws s3 cp s3://[YOUR_RDS_BUCKET_NAME]/config.json config.json
sed -i "s?AWS 플레이트?AWS 플레이트2?" templates/index.html
python main.py
```
9. Launch **ALB** and include two instances.
10. Check if the page shows contents through different EC2 instances.
