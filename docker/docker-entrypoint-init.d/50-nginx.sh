#!/bin/bash -e

# Check for AWS EC2 internal endpoint
if [[ -n $DBMI_LB ]]; then

    # Get the EC2 host IP
    export DBMI_EC2_HOST=$(curl -sL http://169.254.169.254/latest/meta-data/local-ipv4)
    export ALLOWED_HOSTS=$ALLOWED_HOSTS,$DBMI_EC2_HOST

    # Set the trusted addresses for load balancers to the current subnet
    DBMI_EC2_MAC=$(curl -sL http://169.254.169.254/latest/meta-data/mac)
    export DBMI_LB_SUBNET=$(curl -sL http://169.254.169.254/latest/meta-data/network/interfaces/macs/$DBMI_EC2_MAC/vpc-ipv4-cidr-blocks)

fi

# Setup the nginx and site configuration
j2 /docker-entrypoint-templates.d/nginx.healthcheck.conf.j2 > /etc/nginx/conf.d/nginx.healthcheck.conf
j2 /docker-entrypoint-templates.d/nginx.conf.j2 > /etc/nginx/nginx.conf
