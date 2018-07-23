FROM kalilinux/kali-linux-docker
# Metadata params
ARG BUILD_DATE
ARG VERSION
ARG VCS_URL
ARG VCS_REF

LABEL org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.vcs-url=$VCS_URL \
      org.label-schema.vcs-ref=$VCS_REF \
      org.label-schema.version=$VERSION \
      org.label-schema.name='Kali Linux' \
      org.label-schema.description='Official Kali Linux docker image' \
      org.label-schema.usage='https://www.kali.org/news/official-kali-linux-docker-images/' \
      org.label-schema.url='https://www.kali.org/' \
      org.label-schema.vendor='Offensive Security' \
      org.label-schema.schema-version='1.0' \
      org.label-schema.docker.cmd='docker run --rm kalilinux/kali-linux-docker' \
      org.label-schema.docker.cmd.devel='docker run --rm -ti kalilinux/kali-linux-docker' \
      org.label-schema.docker.debug='docker logs $CONTAINER' \
      io.github.offensive-security.docker.dockerfile="Dockerfile" \
      io.github.offensive-security.license="GPLv3" \
      MAINTAINER="Steev Klimaszewski <steev@kali.org>"
      
RUN echo "deb http://http.kali.org/kali kali-rolling main contrib non-free" > /etc/apt/sources.list && \
    echo "deb-src http://http.kali.org/kali kali-rolling main contrib non-free" >> /etc/apt/sources.list

ENV DEBIAN_FRONTEND noninteractive

# Update image and download MSFConsole
RUN apt-get -yqq update \
    && apt-get -yqq dist-upgrade \
    && apt-get install -yqq metasploit-framework \
    && apt-get install -y apache2 \
    && apt-get install -yqq python-pip python-dev \
    && apt-get clean 

WORKDIR /code


# Download set-toolkit
RUN git clone https://github.com/trustedsec/social-engineer-toolkit.git /etc/social-engineer-toolkit \
    && chmod +x /etc/social-engineer-toolkit/setoolkit \
    && pip install pexpect pycrypto requests pyopenssl pefile impacket qrcode pillow \
    && python /etc/social-engineer-toolkit/setup.py install

# Download postfix
RUN apt-get install -yqq postfix \ 
    && git clone https://github.com/galkan/sees \
    && touch /var/log/mail.log \
    && service postfix start 

CMD ["bash"]

# docker run --name kali_container_1 -v ~/Development/kali_docker/utils:/utils -i -t my_kali  /bin/bash
# docker run --name kali_container_2 -v ~/Development/kali_docker/utils:/utils -i -t my_kali_postfix  /bin/bash
# docker run --name kali_container_3 -p 5000:5000 -v ~/Development/kali_docker/code:/code -i -t my_kali_postfix /bin/bash

# python sees.py --text --config_file config/sees.cfg --mail_user config/mail.user  --html_file data/html.text -v
# python sees.py --attach --config_file config/sees.cfg --mail_user config/mail.user  --html_file data/html.text -v


