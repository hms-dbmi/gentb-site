FROM python:3.7-slim AS builder

# Install some pip packages
RUN pip install awscli boto3 shinto-cli dumb-init gunicorn

# Add requirements
ARG BUILD_ENV=prod
ARG APP_ROOT=/var/gentb/app
ADD requirements.txt ${APP_ROOT}/requirements.txt
ADD requirements ${APP_ROOT}/requirements

# Install requirements
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        ca-certificates \
        bzip2 \
        libfontconfig \
        g++ \
        libssl-dev \
    && pip install -r ${APP_ROOT}/requirements.txt \
    && if test -f ${APP_ROOT}/requirements/${BUILD_ENV}.txt; then pip install -r ${APP_ROOT}/requirements/${BUILD_ENV}.txt; fi

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
ARG APP_ROOT=/var/gentb/app
ADD requirements.txt ${APP_ROOT}/requirements.txt
ADD requirements ${APP_ROOT}/requirements

# Install Python packages
RUN pip install -r ${APP_ROOT}/requirements.txt
RUN if test -f ${APP_ROOT}/requirements/${BUILD_ENV}.txt; then pip install -r ${APP_ROOT}/requirements/${BUILD_ENV}.txt; fi

# Copy app source
COPY ./ ${APP_ROOT}

# Copy scripts, templates and resources
ADD docker/docker-entrypoint-templates.d/ /docker-entrypoint-templates.d/
ADD docker/docker-entrypoint-resources.d/ /docker-entrypoint-resources.d/
ADD docker/docker-entrypoint-init.d/ /docker-entrypoint-init.d/
ADD docker/docker-entrypoint.d/ /docker-entrypoint.d/

# Select runtime scripts/resources based on environment
RUN if test -d ${APP_ROOT}/docker/docker-entrypoint-templates${BUILD_ENV+-$BUILD_ENV}.d; then \
    cp -rf ${APP_ROOT}/docker/docker-entrypoint-templates${BUILD_ENV+-$BUILD_ENV}.d/* /docker-entrypoint-templates.d/; fi
RUN if test -d ${APP_ROOT}/docker/docker-entrypoint-resources${BUILD_ENV+-$BUILD_ENV}.d; then \
    cp -rf ${APP_ROOT}/docker/docker-entrypoint-resources${BUILD_ENV+-$BUILD_ENV}.d/* /docker-entrypoint-resources.d/; fi
RUN if test -d ${APP_ROOT}/docker/docker-entrypoint-init${BUILD_ENV+-$BUILD_ENV}.d; then \
    cp -rf ${APP_ROOT}/docker/docker-entrypoint-init${BUILD_ENV+-$BUILD_ENV}.d/* /docker-entrypoint-init.d/; fi
RUN if test -d ${APP_ROOT}/docker/docker-entrypoint${BUILD_ENV+-$BUILD_ENV}.d; then \
    cp -rf ${APP_ROOT}/docker/docker-entrypoint${BUILD_ENV+-$BUILD_ENV}.d/* /docker-entrypoint.d/; fi

# Set app parameters. These can be overridden in the ECS Task Definition's container environment variables.
ENV DBMI_ENV=${BUILD_ENV}
ENV DBMI_SECRET_MANAGER_ID=/dbmi/gentb/${DBMI_ENV}
ENV DBMI_AWS_REGION=us-east-1
ENV DBMI_APP_WSGI=tb_website
ENV DBMI_APP_ROOT=${APP_ROOT}
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

# Add the init script and make it executable
ADD docker/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod a+x docker-entrypoint.sh

ENTRYPOINT ["dumb-init", "/docker-entrypoint.sh"]

CMD gunicorn ${DBMI_APP_WSGI}.wsgi:application -b unix:${DBMI_GUNICORN_SOCKET} \
    --user ${DBMI_NGINX_USER} --group ${DBMI_NGINX_USER} --chdir=${DBMI_APP_ROOT}