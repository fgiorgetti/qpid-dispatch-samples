# Gets the latest Fedora from dockerhub
FROM fedora:32

LABEL maintainer=fgiorgetti@gmail.com

RUN dnf -y install \
    ca-certificates \
    python3-qpid-proton \
    && dnf clean all -y

# Creates a directory to store application
WORKDIR /opt/server

# Copying scripts
COPY *.py ./

# Exposed port
EXPOSE 8080

# runs sender.py by default
CMD python3 current_time_server.py
