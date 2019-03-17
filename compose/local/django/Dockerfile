FROM python:3.6

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y --no-install-recommends gettext && apt-get clean

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install -r /requirements/local.txt

COPY ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r//' /entrypoint
RUN chmod +x /entrypoint


WORKDIR /app

ENTRYPOINT ["/entrypoint"]
