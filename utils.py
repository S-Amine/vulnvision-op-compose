import secrets
import string
import sys
import os
import subprocess
import selectors
import time

def install_docker_ubuntu():
    os.system("sudo apt-get update")
    os.system("sudo apt-get install ca-certificates curl gnupg")
    os.system("sudo install -m 0755 -d /etc/apt/keyrings")
    os.system("curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg")
    os.system("sudo chmod a+r /etc/apt/keyrings/docker.gpg")
    os.system('''echo \
"deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
"$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
sudo tee /etc/apt/sources.list.d/docker.list > /dev/null''')
    os.system("sudo apt-get update")
    os.system("sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin")
    os.system("sudo usermod -a -G docker $USER")
    os.system("sudo chmod 777 /var/run/docker.sock")


def install_os_dependencies_ubuntu():
    install_docker_ubuntu()

def introduction():
    logo = """
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
    """

    description = """
The script you provided is an auto deploy script for a Docker Compose environment. It sets up various microservices and generates configuration files based on user input.

Before starting the script, you'll need to gather the following information:

    1. API Domain: IP domain for the Vulnvision OP App.

Once you provide the required information, the script will generate configuration files, including nginx.conf for Nginx, environment files for each microservice, and RabbitMQ environment files. These files will be used to configure and deploy the Docker Compose environment.
    """

    colored_logo = ""

    delay = 0.0045  # Delay in seconds between each letter
    for char in logo:
        if char == "," or char == ".":
            colored_logo += "\033[31m" + char + "\033[0m"  # Set color to red
        else:
            colored_logo += "\033[37m" + char + "\033[0m"  # Set color to white

    print(colored_logo)

    sel = selectors.DefaultSelector()
    sel.register(sys.stdin, selectors.EVENT_READ)

    for char in description:
        print(char, end="", flush=True)  # Print the character without a newline
        time.sleep(delay)  # Pause for the specified delay

        if sel.select(timeout=0):
            delay = 0

def generate_random_password(length=10):
    # Define the characters to include in the password
    characters = string.ascii_letters + string.digits + "@*"
    # Generate the password
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password

def transform_url(url):
    # Remove "https://" or "http://" from the beginning of the URL
    if url.startswith("https://"):
        url = url[8:]
    elif url.startswith("http://"):
        url = url[7:]

    # Remove any trailing slashes
    url = url.rstrip("/")

    return url

def microservice_env_content(DJANGO_DB_NAME,DJANGO_DB_USER,DJANGO_DB_PASSWORD,DJANGO_RABBITMQ_HOST,DJANGO_RABBITMQ_USER,DJANGO_RABBITMQ_PASSWORD, FINDIP_TOKEN=None):
    FINDIP_TOKEN_ENV= ""
    if FINDIP_TOKEN != None :
        FINDIP_TOKEN_ENV= f"FINDIP_TOKEN={FINDIP_TOKEN}"
    content = f"""
DJANGO_DB_NAME={DJANGO_DB_NAME}
DJANGO_DB_USER={DJANGO_DB_USER}
DJANGO_DB_PASSWORD={DJANGO_DB_PASSWORD}
DJANGO_RABBITMQ_HOST={DJANGO_RABBITMQ_HOST}
DJANGO_RABBITMQ_USER={DJANGO_RABBITMQ_USER}
DJANGO_RABBITMQ_PASSWORD={DJANGO_RABBITMQ_PASSWORD}
{FINDIP_TOKEN_ENV}
    """
    return content

def postgres_env_content(DJANGO_DB_NAME,DJANGO_DB_USER,DJANGO_DB_PASSWORD):
    content = f"""POSTGRES_DB={DJANGO_DB_NAME}
POSTGRES_USER={DJANGO_DB_USER}
POSTGRES_PASSWORD={DJANGO_DB_PASSWORD}
POSTGRES_HOST_AUTH_METHOD=trust
    """
    return content

def generate_folder_file(file_name, content, folder_name="env_files"):
    try:
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        file_path = os.path.join(folder_name, file_name)
        with open(file_path, "w") as file:
            file.write(content)
        print(f"File '{file_name}' created successfully in '{folder_name}/' folder.")
    except Exception as e:
        print(f"An error occurred while creating the file: {str(e)}")

def create_nginx_conf(API_SERVER_NAME, WEBSOCKET_SERVER_NAME, PORTAINER_SERVER_NAME, GRAFANA_SERVER_NAME):
    nginx_conf = """


# vulnvision api
server {
  listen 80;
  server_name """ + API_SERVER_NAME + """;
  location / {
        proxy_set_header Host $http_host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_redirect off;
        if (!-f $request_filename) {
            proxy_pass http://vulnvision:8000;
        }
    }

}

    """
    generate_folder_file(file_name="nginx-setup.conf", content=nginx_conf, folder_name="nginx")

def create_rabbitmq_env(VULNVISION_DJANGO_RABBITMQ_USER, VULNVISION_DJANGO_RABBITMQ_PASSWORD, NUCLEI_DJANGO_RABBITMQ_USER, NUCLEI_DJANGO_RABBITMQ_PASSWORD, NMAP_DJANGO_RABBITMQ_USER, NMAP_DJANGO_RABBITMQ_PASSWORD):
    rabbit_mq_content = f"""
RABBITMQ_DEFAULT_USER=admino
RABBITMQ_DEFAULT_PASS=12345678
RABBITMQ_DEFAULT_VHOST=/
RABBITMQ_USERS={VULNVISION_DJANGO_RABBITMQ_USER}:{VULNVISION_DJANGO_RABBITMQ_PASSWORD},{NUCLEI_DJANGO_RABBITMQ_USER}:{NUCLEI_DJANGO_RABBITMQ_PASSWORD},{NMAP_DJANGO_RABBITMQ_USER}:{NMAP_DJANGO_RABBITMQ_PASSWORD}
"""
    generate_folder_file(file_name="rabbitmq.env", content=rabbit_mq_content)
