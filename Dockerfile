FROM ubuntu:latest

RUN sudo apt update
RUN sudo apt install -y graphviz

COPY . /apps/

CMD ["/bin/bash"]
