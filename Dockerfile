FROM python:3.8-slim

WORKDIR /app
ADD requirements.txt /app/

RUN pip install -r requirements.txt

ADD . /app/

EXPOSE 8000
CMD ["hypercorn", "main:app", "--bind", "0.0.0.0:8000", "--reload"]