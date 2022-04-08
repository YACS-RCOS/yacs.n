FROM python:3.8

RUN mkdir -p /usr/src
WORKDIR /usr/src
COPY ./../requirements.txt /usr/src/
RUN pip install --no-cache-dir -r requirements.txt
COPY ../ /usr/src/

CMD [ "sh", "tests/test.sh" ]
