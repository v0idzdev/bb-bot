#!/bin/bash

screen
sleep 0.5 && xdotool key 'Return' # Return out of screen

python3 -m pip install -r requirements.txt
python3 app.py

xdotool getactivewindow key ctrl+a