FROM python:3.8
WORKDIR /code
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
ENTRYPOINT [“gunicorn”, “project_name.wsgi:application”, “--bind”, “0.0.0.0:8000”]