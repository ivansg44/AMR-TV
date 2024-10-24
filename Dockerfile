FROM python:3.9.20-slim

COPY . .

RUN pip install -r requirements.txt

CMD [ "gunicorn", "--workers=5", "--threads=1", "-b 0.0.0.0:8050", "app:server"]
