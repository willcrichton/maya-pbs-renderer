#!/bin/bash
if [ "$1" == "on" ]; then
    echo "Enabling cron"
    crontab -l | sed "/^#.*fix/s/^#//" | crontab -
else
    echo "Disabling cron"
    crontab -l | sed "/^[^#].*fix/s/^/#/" | crontab -
fi