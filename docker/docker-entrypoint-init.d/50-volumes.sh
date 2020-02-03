#!/bin/bash -e

# Ensure proper permissions are set on storage
echo "${GENTB_SHARED_ROOT}: Setting owner to ${DBMI_NGINX_USER} and permissions to 775"
chown -R ${DBMI_NGINX_USER}:${DBMI_NGINX_USER} ${GENTB_SHARED_ROOT}
chmod -R 775 ${GENTB_SHARED_ROOT}
