FROM python:stretch

WORKDIR /usr/src/insults

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5432

RUN python -m spacy download en
RUN python insults.py
