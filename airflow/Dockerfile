# syntax=docker/dockerfile:1
#######################################################################
# Base image (Airflow 2.10.5 on Python 3.11)                          #
#######################################################################
FROM apache/airflow:2.10.5-python3.11

#######################################################################
# ── Root layer: install gcloud SDK & useful tools ───────────────────#
#######################################################################
USER root

RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
        curl wget gnupg ca-certificates lsb-release; \
    echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" \
        > /etc/apt/sources.list.d/google-cloud-sdk.list; \
    curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg \
        | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg; \
    apt-get update && apt-get install -y --no-install-recommends google-cloud-cli; \
    apt-get clean && rm -rf /var/lib/apt/lists/*

#######################################################################
# ── Back to the airflow user: Python deps with constraints ───────── #
#######################################################################
USER airflow
ENV AIRFLOW_HOME=/opt/airflow
WORKDIR ${AIRFLOW_HOME}

# Copy any extra Python requirements you maintain
COPY requirements.txt ${AIRFLOW_HOME}/requirements.txt

# Tell pip to respect the official constraints file
ENV AIRFLOW_VERSION=2.10.5
ENV PYTHON_VERSION=3.11
ENV CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"

RUN --mount=type=cache,target=/home/airflow/.cache/pip \
    pip install --no-cache-dir \
        -r requirements.txt \
        "apache-airflow-providers-google" \
        --constraint "${CONSTRAINT_URL}"

#######################################################################
# ── Install dbt separately to avoid constraints conflicts ──────────#
#######################################################################
RUN --mount=type=cache,target=/home/airflow/.cache/pip \
    pip install --no-cache-dir dbt-core dbt-bigquery

#######################################################################
# ── copy GCP credentials & expose default path ─────────── #
#######################################################################
COPY ./google ${AIRFLOW_HOME}/google
ENV GOOGLE_APPLICATION_CREDENTIALS=${AIRFLOW_HOME}/google/credentials.json

# (Nothing else needed—entrypoints come from the base image)
