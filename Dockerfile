FROM registry.hpc.ut.ee/mirror/library/ubuntu:20.04 
#AS app

#chooses the default settings
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install --no-install-recommends -y \
    nginx \
    wget \
    supervisor \
    gnupg \
    ca-certificates \
    gettext-base \
    build-essential \
    python3-setuptools \
    python3-pip \
    python3.8 \
    python3.8-venv \
    tesseract-ocr \ 
    ffmpeg \
    libsm6 \ 
    libxext6 \ 
    #git \
    && rm -rf /var/lib/apt/lists/*


#chooses the default settings
RUN apt-get update && apt-get install --no-install-recommends -yqq \
    ca-certificates \
    gettext-base \
    curl 

RUN curl -sL https://deb.nodesource.com/setup_16.x  | bash -
RUN apt-get install -y nodejs
RUN npm install -g npm@9


COPY docker/supervisord.conf /etc/supervisord.conf
COPY docker/nginx.conf /etc/nginx/nginx.conf

RUN mkdir /run/gunicorn/
COPY docker/gunicorn_conf.py /etc/gunicorn_conf.py

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN pip install gunicorn 

WORKDIR /opt

COPY client ./client
COPY server ./server
COPY scripts ./scripts


WORKDIR /opt/scripts
RUN pip install -e .


WORKDIR /opt/client


RUN npm install cross-env
RUN npm install
RUN npm run build 

ENV PATH="/opt/:$PATH"
ENV PYTHONPATH="/opt/:$PYTHONPATH"
ENV PYTHONPATH="/opt/scripts:$PYTHONPATH"

WORKDIR /opt

EXPOSE 80/tcp
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]

