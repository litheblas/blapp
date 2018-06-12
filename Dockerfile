FROM alpine:3.7

# PIP_NO_CACHE_DIR=false actually means *no cache*
ENV APP_ROOT=/app
ENV DJANGO_SETTINGS_MODULE=blapp.settings \
    PATH=${APP_ROOT}/bin:${PATH} \
    PIP_NO_CACHE_DIR=false \
    PIPENV_DONT_LOAD_ENV=true \
    PYTHONUNBUFFERED=true

RUN mkdir ${APP_ROOT}
WORKDIR ${APP_ROOT}

COPY apk-packages.txt ${APP_ROOT}/
RUN apk add --no-cache $(grep -vE "^\s*#" ${APP_ROOT}/apk-packages.txt | tr "\r\n" " ") && \
    pip3 install -U "pipenv!=9.0.0"

COPY Pipfile Pipfile.lock ${APP_ROOT}/
RUN pipenv install --system --deploy

COPY package.json yarn.lock ${APP_ROOT}/
RUN yarn install && yarn cache clean

COPY . ${APP_ROOT}/

RUN pip3 install -e ${APP_ROOT} && \
    yarn prod-build && \
    BLAPP_DATABASE_URL=sqlite://// BLAPP_LEGACY_DATABASE_URL=sqlite://// BLAPP_EMAIL_URL=consolemail:// BLAPP_REDIS_URL=redis:// BLAPP_SECRET_KEY=build django-admin collectstatic --no-input

EXPOSE 80
CMD ["web-server"]
