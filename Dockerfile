FROM ubuntu:22.04

RUN apt update && apt install -y \
    build-essential \
    git \
    m4 \
    scons \
    python3 \
    python3-pip \
    python3-dev \
    zlib1g-dev \
    protobuf-compiler \
    libprotobuf-dev \
    libgoogle-perftools-dev \
    libboost-all-dev \
    pkg-config \
    vim \
    wget

WORKDIR /gem5

COPY . /gem5

RUN scons build/X86/gem5.opt -j$(nproc)

CMD ["/bin/bash"]