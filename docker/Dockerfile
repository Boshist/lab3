FROM python:3
WORKDIR /app
COPY . /app
RUN apt-get update
RUN pip install -r requirements.txt
CMD python server.py
EXPOSE 5000