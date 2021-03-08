FROM ubuntu:latest

RUN apt install -y graphviz

COPY . /apps/

CMD ["/bin/bash"]
