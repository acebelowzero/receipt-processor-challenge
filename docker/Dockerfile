FROM python:3.12-slim as base

# setup env
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# Build base
FROM base as build-stage
RUN pip install poetry
WORKDIR $PYSETUP_PATH
COPY ./poetry.lock ./pyproject.toml ./
RUN poetry install


FROM base as production
ENV FASTAPI_ENV=production
COPY --from=build-stage $VENV_PATH $VENV_PATH

# Create a user with UID 1234 and GID 1234
RUN groupadd -g 1234 receipt && \
    useradd -m -u 1234 -g receipt receipt

RUN mkdir /opt/temp && chown -R receipt /opt/temp

USER receipt

COPY ./ /opt/temp
WORKDIR /opt/temp
EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]