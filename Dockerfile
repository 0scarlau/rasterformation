FROM python:3.6-alpine

COPY ./rasterformation ./opt/rasterformation/
RUN \
    apk --no-cache --update-cache add gcc gfortran python python-dev py-pip build-base wget freetype-dev libpng-dev openblas-dev && \
    apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev && \
    addgroup -g 2000 raster && \
    adduser -u 2000 -G raster -D raster -s /usr/sbin/nologin && \
    chown -R raster:raster /opt/rasterformation/* && \
    cd /opt/rasterformation/src && \
    pip install --upgrade setuptools && \
    pip install -r requirements.txt

USER raster
WORKDIR /opt/rasterformation/

ENTRYPOINT ["python"]
CMD ["raster_transformation_app.py"]