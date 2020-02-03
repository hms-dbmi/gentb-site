#!/bin/bash

if [[ -n $GENTB_INITIAL_EMAIL && -n $GENTB_INITIAL_PASSWORD ]]; then
    echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('$GENTB_INITIAL_EMAIL', '$GENTB_INITIAL_EMAIL', '$GENTB_INITIAL_PASSWORD')" | python /app/manage.py shell || echo "Admin already set"
fi