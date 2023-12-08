#!/bin/bash

# Update your existing list of packages
sudo apt update -y ;

# Install a few prerequisite packages which let apt use packages over HTTPS
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common ;

# Add the GPG key for the official Docker repository to your system
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -  ;

# Add the Docker repository to APT sources
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"  ;

# Update the package database with the Docker packages from the newly added repo
sudo apt update -y  ;

# Make sure you are about to install from the Docker repo instead of the default Ubuntu repo
apt-cache policy docker-ce  ;

# Install Docker
sudo apt install -y docker-ce  ;

# Execute Docker command without sudo
sudo usermod -aG docker ${USER}  ;

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose  ;

# Apply executable permissions to the Docker Compose binary
sudo chmod +x /usr/local/bin/docker-compose  ;

# Install npm
sudo apt install -y npm  ;

# Install PM2
sudo npm install -g pm2  ;

# Install python requirements

pip install -r requirements.txt ;

# Test installation
docker --version
docker-compose --version
npm --version
pm2 --version
