FROM python:3.8.6

RUN mkdir /www/fengfeng_blog -p
WORKDIR /www/fengfeng_blog

COPY ../../requirements.txt /www/fengfeng_blog
RUN ls && pip install --no-cache-dir -r requirements.txt \
    && pip install uwsgi

RUN uwsgi --ini myweb_uwsgi.ini

#ENTRYPOINT ["/bin/bash", "entrypoint.sh"]