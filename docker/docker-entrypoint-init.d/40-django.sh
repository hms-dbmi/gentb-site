#!/bin/bash -e

# Run migrations
echo "${DBMI_APP_MEDIA_ROOT}: Running migrate"
python ${DBMI_APP_ROOT}/manage.py migrate --no-input

# Check for static files
if [[ -n $DBMI_APP_STATIC_ROOT ]]; then

    # Ensure proper permissions are set on static root
    echo "${DBMI_APP_STATIC_ROOT}: Setting owner to ${DBMI_NGINX_USER} and permissions to 775"
    mkdir -p "${DBMI_APP_STATIC_ROOT}"
    chown -R ${DBMI_NGINX_USER}:${DBMI_NGINX_USER} ${DBMI_APP_STATIC_ROOT}
    chmod -R 775 ${DBMI_APP_STATIC_ROOT}

    # Make the directory and collect static files
    python ${DBMI_APP_ROOT}/manage.py collectstatic --no-input

fi

# Check for media files
if [[ -n $DBMI_APP_MEDIA_ROOT ]]; then

    # Ensure proper permissions are set on static root
    echo "${DBMI_APP_MEDIA_ROOT}: Setting owner to ${DBMI_NGINX_USER} and permissions to 775"
    mkdir -p "${DBMI_APP_MEDIA_ROOT}"
    chown -R ${DBMI_NGINX_USER}:${DBMI_NGINX_USER} ${DBMI_APP_MEDIA_ROOT}
    chmod -R 775 ${DBMI_APP_MEDIA_ROOT}

    # Make the directory and collect media files
    python ${DBMI_APP_ROOT}/manage.py collectmedia --noinput

fi