FROM python:3.9.20-slim

COPY . .

RUN pip install -r requirements.txt \
    && apt-get update \
    && apt-get install gcc g++ gdb make libtool autoconf automake pkg-config -y \
    && cd adaptagrams/cola \
    && ./autogen.sh \
    && make install \
    && ./buildPythonSWIG.sh \
    && cd ../..

CMD [ "gunicorn", "--workers=5", "--threads=1", "-b 0.0.0.0:8050", "app:server"]
