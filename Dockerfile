#
# Build image
#
FROM python:3.10-slim-bullseye AS builder

WORKDIR /app
COPY pyproject.toml poetry.lock ./

ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"

# Install poetry
RUN DEBIAN_FRONTEND=noninteractive apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && curl -sSL https://install.python-poetry.org | python3 -

# Poetry
RUN poetry config virtualenvs.create false
RUN poetry config warnings.export false
RUN poetry install --only main
RUN poetry self add poetry-plugin-export
RUN poetry export -f requirements.txt --output requirements.txt

# Set time server to Moscow
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

#
# Prod image
#
FROM python:3.10-slim-bullseye AS runtime

WORKDIR /app
COPY evtc_bot /app/evtc_bot
COPY --from=builder /app/requirements.txt /app

ENV PIP_ROOT_USER_ACTION=ignore
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt

CMD ["python", "-m", "evtc_bot"]
