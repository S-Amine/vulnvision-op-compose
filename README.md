# Vulnvision OP

## Installation Guide

Follow these steps to install and configure the repository:

## Prerequisites

Ensure you have Git and Python 3 installed on your Ubuntu machine.

### 1. Clone the Repository

```bash
git clone https://github.com/S-Amine/vulnvision-op-compose/
```

Then cd to the repo :

```bash
cd vulnvision-op-compose
```
### 2. Run the Installation Script

```bash
python3 install.py
```

### 3. Provide Information

If your machine already has a static IP address, enter 'Y' when prompted. Otherwise, type 'n' and set up a static IP address for your host before proceeding with the reinstall.

```bash
@@@@@@
,,,,,,      @@@@@@
 ,,,,,,    @      @@@@@@@
  ,,,,,,    @@@@@@                            ..          ..
   ,,,,,, ,,,,,,         @@                  ....        ....
    ,,,,,,,,,,,  @@  @@  @@  @@@@   @@     @@ ..    @@@@  ..    @@@    @@@@
     ,,,,,,,,,   @@  @@  @@  @@  @@  @@   @@  @@  @@      @@  @@   @@  @@  @@
      ,,,,,,,    @@  @@  @@  @@  @@   @@ @@   @@  @@@@@@  @@  @@   @@  @@  @@
       ,,,,,     @@  @@  @@  @@  @@    @@@    @@      @@  @@  @@   @@  @@  @@
        ,,,      @@@@@@  @@  @@  @@     @     @@  @@@@@   @@    @@@    @@  @@

The script you provided is an auto deploy script for a Docker Compose environment. It sets up various microservices and generates configuration files based on user input.

Before starting the script, you'll need to gather the following information:

    1. API Domain: IP domain for the Vulnvision OP App.

Once you provide the required information, the script will generate configuration files, including nginx.conf for Nginx, environment files for each microservice, and RabbitMQ environment files. These files will be used to configure and deploy the Docker Compose environment.

Do you have these informations [y/n] : Y
```

If you already have a static IP, enter the actual <ip_address> in the next input:

```bash
Please enter the IP Address of this host : <ip_address>
```

Please provide the sudo password for the installation of dependencies. Note that the sudo password is not stored and is used solely by open-source commands in the 'os_dep.sh' file.

```bash
[sudo] password for <user>:
```

### 4. Access the Application

Once the installation is complete, you can access the application at:

- http://INPUT_API_DOMAIN:8000
- http://INPUT_API_DOMAIN:80

Default credentials:

- Username: admin@admin.com
- Password: adminadmin
