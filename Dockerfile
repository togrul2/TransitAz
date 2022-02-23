FROM python:3.9
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /transitaz
COPY requirements.txt /transitaz/
RUN pip install -r requirements.txt
COPY . /transitaz/
