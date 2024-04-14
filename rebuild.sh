#!/bin/sh
docker stop container-critique
docker rm container-critique
docker build . -t tiyn/container-critique
docker run --name container-critique \
    --restart unless-stopped \
    -p "5001:5000" \
    -e FLASK_ENV=development \
    -v data:/blog/data \
    -v graphics:/blog/static/graphics \
    -d tiyn/container-critique
