#!/bin/bash -e

# Ensure proper permissions are set on app root
echo "${DBMI_APP_ROOT}: Setting owner to ${DBMI_NGINX_USER} and permissions to 775"
chown -R ${DBMI_NGINX_USER}:${DBMI_NGINX_USER} ${DBMI_APP_ROOT}
chmod -R 775 ${DBMI_APP_ROOT}
