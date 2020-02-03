#!/bin/bash -e

# Copy GenTb bin directory to shared root
echo "${DBMI_APP_ROOT}/bin: Copying GenTb app bin to shared volume: ${GENTB_SHARED_ROOT}/bin"
mkdir -p ${GENTB_SHARED_ROOT}/bin
cp -rf ${DBMI_APP_ROOT}/bin/* ${GENTB_SHARED_ROOT}/bin/

# Ensure proper permissions are set on storage
echo "${GENTB_SHARED_ROOT}: Setting owner to ${DBMI_NGINX_USER} and permissions to 775"
chown -R ${DBMI_NGINX_USER}:${DBMI_NGINX_USER} ${GENTB_SHARED_ROOT}
chmod -R 775 ${GENTB_SHARED_ROOT}
