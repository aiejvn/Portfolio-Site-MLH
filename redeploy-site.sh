#!/bin/bash

cd /root/Portfolio-Site-MLH
git fetch
git reset origin/main --hard
chmod +x ./redeploy-site.sh
cd ./python3-virtualenv
source ./bin/activate
pip install -r ../requirements.txt
systemctl daemon-reload
systemctl restart myportfolio
