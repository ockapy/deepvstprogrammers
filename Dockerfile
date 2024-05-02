# On utilise python 3.9
FROM python:3.9.10

# Mise en place du workdir dans le conteneur
WORKDIR /app

# Copie les fichiers nécessaires dans le conteneur
ADD ./app /app/Program
ADD ./RenderMan /app/Renderman
COPY requirements.txt .


# Installation des prérequis
RUN apt-get update && apt-get install -y \
    python3-dev \
    libpq-dev build-essential \
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
    libcurl4-gnutls-dev

# Installation des packages python
RUN pip install --no-cache-dir -r requirements.txt


# Permet de trouver le fichier pyconfig.h et de compiler RenderMan


RUN wget https://boostorg.jfrog.io/artifactory/main/release/1.85.0/source/boost_1_85_0.tar.bz2 && \
tar --bzip2 -xf boost_1_85_0.tar.bz2 && \
cd boost_1_85_0 && \
./bootstrap.sh --with-libraries=python --with-python=python3.9 --prefix=/usr/local && \
./b2 install

RUN cd RenderMan/Builds/LinuxMakefile
RUN export CPLUS_INCLUDE_PATH="$CPLUS_INCLUDE_PATH:/usr/include/python3.9"
RUN export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

