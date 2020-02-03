#!/bin/bash -e

# We need to dump the current environment to a file for cron processes to pickup
declare -p | grep -Ev 'BASHOPTS|BASH_VERSINFO|EUID|PPID|SHELLOPTS|UID' > /cron.env

# Generate cron file
j2 /docker-entrypoint-templates.d/gentb-cron.j2 > /etc/cron.d/gentb-cron
chmod +x /etc/cron.d/gentb-cron