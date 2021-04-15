FROM openjdk:8-alpine

ARG VERSION=0.20.2
ENV DRUID_PKG=https://downloads.apache.org/druid/${VERSION}/apache-druid-${VERSION}-bin.tar.gz

WORKDIR /opt/druid
RUN apk add --no-cache bash perl
RUN cd /tmp && wget --no-verbose -O druid-${VERSION}.tar.gz ${DRUID_PKG} && mkdir -p /opt/druid && \
    tar xf /tmp/druid-${VERSION}.tar.gz  -C /opt/druid --strip-components=1
#COPY . /usr/src/myapp

#RUN javac Main.java
CMD ["bash", "./bin/start-micro-quickstart"]