#
# ESVk2Pod microservice
#
### Build
# docker build -t esvk2pod .
#
### Run
# docker run -d --name esvk2pod -p 8080:8080 esvk2pod
#   or
# docker run -d --name esvk2pod -e URLPREF=DOMAINNAME -p 8080:8080 esvk2pod
#
### Removing container and image
# docker stop esvk2pod
# docker rm esvk2pod
# docker rmi esvk2pod
#
### Additional info
# You can find code here:
#    https://github.com/alive-corpse/esvk2pod
#
# You also can build python code into portable binaries with nuitka
#    http://nuitka.net/

FROM alpine:3.4
MAINTAINER Evgeniy Shumilov <evgeniy.shumilov@gmail.com>

ARG GLIB=2.23-r1
ARG PYPY=5.6-linux_x86_64-portable

RUN apk update && apk upgrade && apk add curl && apk add libbz2 && mkdir -p /opt/esvk2pod && cd /opt && \
    curl -L -o glibc-$GLIB.apk "https://github.com/sgerrand/alpine-pkg-glibc/releases/download/$GLIB/glibc-$GLIB.apk" && \
    curl -L -o glibc-bin-$GLIB.apk  "https://github.com/sgerrand/alpine-pkg-glibc/releases/download/$GLIB/glibc-bin-$GLIB.apk" && \
    apk add --allow-untrusted glibc-$GLIB.apk glibc-bin-$GLIB.apk && \
    rm -fr glibc-$GLIB.apk glibc-bin-$GLIB.apk /var/cache/apk/* 

RUN cd /opt && curl -L -o pypy-$PYPY.tar.bz2 "https://bitbucket.org/squeaky/portable-pypy/downloads/pypy-$PYPY.tar.bz2" && tar xvjf pypy-$PYPY.tar.bz2 && rm pypy-$PYPY.tar.bz2 && \
    export LC_ALL=C && \
    /opt/pypy-$PYPY/bin/pypy -m ensurepip && \
    ln -s /opt/pypy-$PYPY/bin/pypy /usr/local/bin/pypy && \
    ln -s /opt/pypy-$PYPY/bin/pypy /usr/local/bin/python && \
    ln -s /opt/pypy-$PYPY/bin/pip /usr/local/bin/pip && \
    ln -s /opt/pypy-$PYPY/bin/virtualenv-pypy /usr/local/bin/virtualenv && \
    ln -s /opt/pypy-$PYPY/bin/easy_install /usr/local/bin/easy_install && \
    pip install --upgrade pip && \
    pip install requests

ADD . /opt/esvk2pod/

EXPOSE 8080

ARG URLPREF=localhost

ENTRYPOINT /opt/esvk2pod/esvk2pod.py 8080 127.0.0.1 $URLPREF

