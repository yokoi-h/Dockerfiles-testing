FROM ubuntu:14.04

RUN apt-get update
RUN apt-get install -qy --no-install-recommends python-setuptools python-pip git emacs24-nox

ENV HOME /root
WORKDIR /root
ADD book /root/book/
RUN cd /root/book && pip install -r requirements.txt
WORKDIR /root/book
CMD ["/usr/bin/python", "/root/book/app.py"]

