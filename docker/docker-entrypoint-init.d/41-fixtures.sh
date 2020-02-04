#!/bin/bash -e

echo "${DBMI_APP_MEDIA_ROOT}/mutations: Installing fixtures drugs.json"
python ${DBMI_APP_ROOT}/manage.py loaddata ${DBMI_APP_ROOT}/apps/mutations/fixtures/drugs.json

echo "${DBMI_APP_MEDIA_ROOT}/mutations: Installing fixtures genelocus.json"
python ${DBMI_APP_ROOT}/manage.py loaddata ${DBMI_APP_ROOT}/apps/mutations/fixtures/genelocus.json

echo "${DBMI_APP_MEDIA_ROOT}/tb_website: Installing fixtures basic_pipelines.json"
python ${DBMI_APP_ROOT}/manage.py loaddata ${DBMI_APP_ROOT}/tb_website/fixtures/basic_pipelines.json
