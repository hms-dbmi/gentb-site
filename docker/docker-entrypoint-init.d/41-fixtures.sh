#!/bin/bash -e

python /app/manage.py loaddata /app/apps/mutations/fixtures/drugs.json
python /app/manage.py loaddata /app/apps/mutations/fixtures/genelocus.json
python /app/manage.py loaddata /app/tb_website/fixtures/basic_pipelines.json
