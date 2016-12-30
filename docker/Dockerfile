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

FROM debian:latest
MAINTAINER Evgeniy Shumilov <evgeniy.shumilov@gmail.com>

RUN apt-get update; apt-get -y upgrade; apt-get -y autoremove; apt-get install -y python python-requests busybox
ADD https://github.com/alive-corpse/esvk2pod/archive/master.zip /opt
RUN busybox unzip /opt/master.zip -d /opt; rm /opt/master.zip
ARG URLPREF=localhost
RUN echo -e '#!/bin/sh\nIFACE=`busybox route -n | awk '"'"'$1~/^0\.0\.0\.0$/ { print $NF }'"'"'`\nIP=`busybox ifconfig $IFACE | awk '"'"'$1~/^inet$/ { gsub(/addr:/,"",$2); print $2 }'"'"'`\n/opt/esvk2pod-master/esvk2pod.py 8080 $IP $URLPREF' > /opt/starter.sh; chmod +x /opt/starter.sh

EXPOSE 8080
ENTRYPOINT /opt/starter.sh
