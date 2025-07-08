FROM ghcr.io/prefix-dev/pixi:0.48.2

COPY . .

RUN pixi install \
    && pixi run compile \
    && pixi shell-hook -e default -s bash > shell-hook \
    && echo "#!/bin/bash" > entrypoint.sh \
    && cat shell-hook >> entrypoint.sh \
    && echo 'exec "$@"' >> entrypoint.sh \
    && chmod 755 entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]

CMD [ "gunicorn", "--workers=5", "--threads=1", "-b 0.0.0.0:8050", "app:server"]
