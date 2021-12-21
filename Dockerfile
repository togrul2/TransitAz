FROM python:3
COPY . /transitaz-prod
WORKDIR /transitaz-prod
RUN pip install -r requirements.txt
CMD python manage.py runserver
