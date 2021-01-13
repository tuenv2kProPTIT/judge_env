FROM ubuntu:18.04
WORKDIR /opt/
RUN apt-get update -y && apt-get upgrade -y 
ENV PYTHONUNBUFFERED=1 C_FORCE_ROOT=true
ENV RABBITMQ_HOST=rabbitmq RABBITMQ_PORT=5672 RABBITMQ_USER=guest RABBITMQ_PWD=guest
ENV POSTGRESQL_HOST=localhost POSTGRESQL_PORT=5432 POSTGRESQL_USER=root POSTGRESQL_PWD=root POSTGRESQL_SCHEMA=proptit_judge
ENV REDIS_HOST=localhost REDIS_PORT=6379

RUN mkdir /storage && chmod -R 755 /storage
RUN apt-get install build-essential wget libcap-dev vim libpq-dev -y
ENV GCC_PATH /usr/bin/x86_64-linux-gnu-gcc-7
ENV GPP_PATH /usr/bin/x86_64-linux-gnu-g++-7
# Install Isolate Sandbox
RUN mkdir isolate
COPY . /opt/
RUN cd isolate && make isolate && make install
ENV ISOLATE /opt/isolate/isolate

#Install Java
# RUN apt-get install openjdk-11-jdk-headless -y
# ENV JAVA_PATH /usr/lib/jvm/java-11-openjdk-amd64/bin/java
# ENV JAVAC_PATH /usr/lib/jvm/java-11-openjdk-amd64/bin/javac

# #Install python environment
# RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
# RUN /bin/bash miniconda.sh -b -p /opt/conda && \
#     rm miniconda.sh && \
#     ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
#     echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc

# RUN /opt/conda/bin/conda create -n py3 python=3.7 -y

ENV PY3_PATH /opt/conda/envs/py3/bin/python

RUN apt-get install python3 python3-dev python3-pip -y

ADD ./requirement.txt /opt/sys_requirements.txt
RUN pip3 install --default-timeout 9999 -r sys_requirements.txt