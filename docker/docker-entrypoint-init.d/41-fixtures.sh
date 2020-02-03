#!/bin/bash -e

python ${DBMI_APP_ROOT}/manage.py loaddata ${DBMI_APP_ROOT}/apps/mutations/fixtures/drugs.json
python ${DBMI_APP_ROOT}/manage.py loaddata ${DBMI_APP_ROOT}/apps/mutations/fixtures/genelocus.json
python ${DBMI_APP_ROOT}/manage.py loaddata ${DBMI_APP_ROOT}/tb_website/fixtures/basic_pipelines.json
