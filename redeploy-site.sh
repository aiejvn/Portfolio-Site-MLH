#!/bin/bash

cd /root/Portfolio-Site-MLH
git fetch
git reset origin/main --hard
chmod +x ./redeploy-site.sh
docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml up -d --build
