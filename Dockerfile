FROM python:3

MAINTAINER tiyn tiyn@mail-mk.eu

COPY src /blog

WORKDIR /blog

RUN pip3 install -r requirements.txt

VOLUME /blog/data

VOLUME /blog/static/graphics

EXPOSE 5000

ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]
