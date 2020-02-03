#!/bin/bash -e

# Install the test fork of Chore
pip uninstall --yes chore
pip install https://github.com/hms-dbmi/chore-docker/zipball/master#egg=chore[batch]
