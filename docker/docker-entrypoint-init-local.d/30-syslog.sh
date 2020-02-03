#!/bin/bash -e

# Install syslog for help debugging
apt-get update && apt-get install -y rsyslog
service rsyslog start
