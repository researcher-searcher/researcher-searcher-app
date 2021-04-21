FROM python:3.8

WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt

#CMD ["python", "index.py"]
CMD [ "gunicorn", "--workers=2", "--threads=1", "-b 0.0.0.0:8050", "index:app.server"]
