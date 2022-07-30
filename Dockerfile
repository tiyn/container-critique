FROM python:3

MAINTAINER tiyn tiyn@mail-mk.eu

COPY src /blog

WORKDIR /blog

VOLUME /blog/data

RUN pip3 install -r requirements.txt

VOLUME /blog/templates/entry

EXPOSE 5000

ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]
