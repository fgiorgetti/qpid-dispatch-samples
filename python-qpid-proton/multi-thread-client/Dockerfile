# Gets the latest Fedora from dockerhub
FROM fedora:32

LABEL maintainer=fgiorgetti@gmail.com

# Custom variables
ENV CLIENT_APP ${client_app:-sender.py}

RUN dnf -y install \
    ca-certificates \
    python3-qpid-proton \
    wget \
    iputils \
    net-tools \
    && dnf clean all -y

# Creates a directory to store client scripts
WORKDIR /opt/client

# Copying scripts
COPY *.py ./

# runs sender.py by default
CMD python3 ${CLIENT_APP}
