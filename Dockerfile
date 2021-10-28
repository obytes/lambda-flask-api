FROM python:3.9-slim-buster

# Create app directory
RUN mkdir -p /opt/app
WORKDIR /opt/app

# Install build deps, then run `pip install`, then remove unneeded build deps all in a single step.
RUN set -ex \
    && apt-get update && apt-get install -y \
    gcc \
    git \
    bash \
    make \
    && rm -rf /var/lib/apt/lists/*


COPY src/requirements/test.txt /opt/pip/requirements/test.txt
RUN pip3 install -r /opt/pip/requirements/test.txt

COPY src/requirements/ecs.txt /opt/pip/requirements/ecs.txt
RUN pip3 install -r /opt/pip/requirements/ecs.txt

ADD . ./
RUN chmod +x ./entrypoint.sh

RUN groupadd -g 9898 appuser && useradd -r -u 9898 -g appuser appuser

RUN mkdir /home/appuser
RUN touch /home/appuser/.profile
RUN chmod 777 /home/appuser/.profile
RUN touch /home/appuser/.pythonrc
RUN chmod 777 /home/appuser/.pythonrc

USER appuser

ENV FLASK_APP src/app/runtime/ecs/app.py

EXPOSE 5000

ENTRYPOINT ["sh", "/opt/app/entrypoint.sh"]

