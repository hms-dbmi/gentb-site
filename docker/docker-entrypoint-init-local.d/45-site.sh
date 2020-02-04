#!/bin/bash -e

echo "${DBMI_APP_DOMAIN}: Updating Django Site 1 with actual domain"
python ${DBMI_APP_ROOT}/manage.py shell -c "from django.contrib.sites.models import Site; Site.objects.filter(domain='example.com').update(name='Gentb', domain='${DBMI_APP_DOMAIN}:${DBMI_PORT}')"