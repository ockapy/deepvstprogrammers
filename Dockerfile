# On utilise python 3.9
FROM python:3.9.10

# Mise en place du workdir dans le conteneur
WORKDIR /app

# Copie les fichiers nécessaires dans le conteneur
ADD ./app /app/Program
ADD ./Renderman /app/Renderman
COPY requirements.txt .


# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-dev \
    libpq-dev \
    build-essential \
    llvm \
    clang \
    libfreetype6-dev \
    libx11-dev \
    libxinerama-dev \
    libxrandr-dev \
    libxcursor-dev \
    mesa-common-dev \
    libasound2-dev \
    freeglut3-dev \
    libxcomposite-dev \
    libcurl4-gnutls-dev \
    wget \
    tar

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Download and install Boost
RUN wget https://boostorg.jfrog.io/artifactory/main/release/1.85.0/source/boost_1_85_0.tar.bz2 && \
    tar --bzip2 -xf boost_1_85_0.tar.bz2 && \
    cd boost_1_85_0 && \
    ./bootstrap.sh --with-libraries=python --with-python=python3.9 --prefix=/usr/local && \
    ./b2 install

# Set environment variables
ENV CPLUS_INCLUDE_PATH="/usr/include/python3.9:${CPLUS_INCLUDE_PATH}"
ENV LD_LIBRARY_PATH="/usr/local/lib:${LD_LIBRARY_PATH}"

# Compile RenderMan
RUN cd /app/Renderman/Builds/LinuxMakefile && \
    make && \
    mv build/librenderman.so /app/Program/utils

