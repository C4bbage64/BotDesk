FROM ubuntu:latest
LABEL authors="irfan"

ENTRYPOINT ["top", "-b"]