FROM python:3.7-slim AS builder

# Install some pip packages
RUN pip install awscli boto3 shinto-cli dumb-init gunicorn

# Add requirements
ARG BUILD_ENV=prod
ADD requirements.txt /app/requirements.txt
ADD requirements /app/requirements

# Install requirements
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        ca-certificates \
        bzip2 \
        libfontconfig \
        g++ \
        libssl-dev \
    && pip install -r /app/requirements.txt \
    && if test -f /app/requirements/${BUILD_ENV}.txt; then pip install -r /app/requirements/${BUILD_ENV}.txt; fi

FROM python:3.7-slim

# Copy pip packages from builder
COPY --from=builder /root/.cache /root/.cache

# Install required packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        nginx \
        jq \
        curl \
        openssl \
        wget \
        git \
        libfontconfig \
        binutils \
        libproj-dev \
        gdal-bin \
        libgeoip1 \
        python-gdal \
        cron \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install some pip packages
RUN pip install awscli boto3 shinto-cli dumb-init gunicorn

# Add requirements
ARG BUILD_ENV=prod
ADD requirements.txt /app/requirements.txt
ADD requirements /app/requirements

# Install Python packages
RUN pip install -r /app/requirements.txt
RUN if test -f /app/requirements/${BUILD_ENV}.txt; then pip install -r /app/requirements/${BUILD_ENV}.txt; fi

# Copy app source
COPY ./ /app

# Copy scripts, templates and resources
ADD docker/docker-entrypoint-templates.d/ /docker-entrypoint-templates.d/
ADD docker/docker-entrypoint-resources.d/ /docker-entrypoint-resources.d/
ADD docker/docker-entrypoint-init.d/ /docker-entrypoint-init.d/
ADD docker/docker-entrypoint.d/ /docker-entrypoint.d/

# Select runtime scripts based on environment
RUN if test -d /app/docker/docker-entrypoint-init${BUILD_ENV+-$BUILD_ENV}.d; then \
    cp -n /app/docker/docker-entrypoint-init${BUILD_ENV+-$BUILD_ENV}.d/* /docker-entrypoint-init.d/; fi

# Set app parameters. These can be overridden in the ECS Task Definition's container environment variables.
ENV DBMI_ENV=${BUILD_ENV}
ENV DBMI_SECRET_MANAGER_ID=/dbmi/gentb/${DBMI_ENV}
ENV DBMI_AWS_REGION=us-east-1
ENV DBMI_APP_WSGI=tb_website
ENV DBMI_APP_ROOT=/var/gentb/app
ENV DBMI_APP_DB=true
ENV DBMI_APP_DOMAIN=gentb.hms.harvard.edu

# Static and media files
ENV DBMI_STATIC_FILES=true
ENV DBMI_APP_STATIC_URL_PATH=/static/
ENV DBMI_APP_STATIC_ROOT=/var/gentb/static/
ENV DBMI_MEDIA_FILES=true
ENV DBMI_APP_MEDIA_URL_PATH=/media/
ENV DBMI_APP_MEDIA_ROOT=/mnt/gentb/
ENV DBMI_GUNICORN_SOCKET=/var/gentb/gunicorn.sock

# Set nginx and network parameters
ENV DBMI_PORT=443
ENV DBMI_LB=true
ENV DBMI_SSL=true
ENV DBMI_CREATE_SSL=true
ENV DBMI_HEALTHCHECK=true

# Copy bin directory for pipeline jobs
# This is likely a temporary measure since these
# will be provided as a part of the gentb-job image
# But for now we need them accessible by GenTb
# so it can build the job command
ADD bin ${DBMI_APP_MEDIA_ROOT}bin

# Add the init script and make it executable
ADD docker/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod a+x docker-entrypoint.sh

ENTRYPOINT ["dumb-init", "/docker-entrypoint.sh"]

CMD gunicorn ${DBMI_APP_WSGI}.wsgi:application -b unix:${DBMI_GUNICORN_SOCKET} \
    --user ${DBMI_NGINX_USER} --group ${DBMI_NGINX_USER} --chdir=${DBMI_APP_ROOT}