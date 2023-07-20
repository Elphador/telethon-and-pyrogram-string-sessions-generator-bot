FROM python:3.9

WORKDIR /app

COPY r.txt /app/

RUN pip3 install -r r.txt

COPY . /app

CMD python3 dalle.py
 