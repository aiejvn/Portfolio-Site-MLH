#!/bin/bash

tmux list-sessions
tmux kill-server
cd /root/Portfolio-Site-MLH
git fetch
git reset origin/main --hard
cd ./python3-virtualenv
source ./bin/activate
pip install -r ../requirements.txt
tmux new-session -d -s Portfolio-Website
tmux send-keys -t 0 'cd /root/Portfolio-Site-MLH' C-m
tmux send-keys -t 0 'export FLASK_ENV=development' C-m
tmux send-keys -t 0 'flask run --host=0.0.0.0' C-m