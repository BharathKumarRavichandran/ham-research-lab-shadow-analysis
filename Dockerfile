FROM python:3.9.7-slim

RUN apt-get update

WORKDIR /usr/src/app

COPY requirements.txt requirements.txt

RUN pip3 install --upgrade pip
RUN pip3 install --upgrade setuptools
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5000

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
