FROM alpine:3.7

# PIP_NO_CACHE_DIR=false actually means *no cache*
ENV APP_ROOT=/app
ENV DJANGO_SETTINGS_MODULE=blapp.settings \
  LANG=en_US.UTF-8 \
  PATH=${APP_ROOT}/bin:${PATH} \
  PIP_NO_CACHE_DIR=false \
  PIPENV_DONT_LOAD_ENV=true \
  PYTHONUNBUFFERED=true

RUN mkdir ${APP_ROOT}
WORKDIR ${APP_ROOT}

COPY apk-packages.txt ${APP_ROOT}/
RUN apk add --no-cache $(grep -vE "^\s*#" ${APP_ROOT}/apk-packages.txt | tr "\r\n" " ") && \
  pip3 install -U "pipenv==2018.11.26"

COPY Pipfile Pipfile.lock ${APP_ROOT}/
# Workaround for https://github.com/pypa/pip/issues/6197 until pip==19.0.2
ENV PIP_USE_PEP517=false
RUN pipenv install --deploy

COPY package.json yarn.lock ${APP_ROOT}/
RUN yarn install && yarn cache clean

COPY . ${APP_ROOT}/

RUN pipenv run pip install -e ${APP_ROOT} && \
  yarn prod-build && \
  BLAPP_DATABASE_URL=sqlite://// BLAPP_LEGACY_DATABASE_URL=sqlite://// BLAPP_EMAIL_URL=consolemail:// BLAPP_REDIS_URL=redis:// BLAPP_SECRET_KEY=build pipenv run django-admin collectstatic --no-input

ARG with_dev_packages
RUN test -z "${with_dev_packages}" || pipenv install --deploy --dev

EXPOSE 80
CMD ["pipenv", "run", "web"]
