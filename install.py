from utils import *
import os
from getpass import getpass

introduction()

answer = None

while answer not in ("y", "n"):
    answer = input("Do you have these informations [y/n] : ")
    if answer.lower() == "y":
        # Input API domain
        INPUT_API_DOMAIN = input("\n Please enter the API domain: ")

        # Input Socket domain
        INPUT_WEBSOCKET_DOMAIN = input("\n Please enter the WebSocket domain: ")

        # Input Portainer domain
        INPUT_PORTAINER_DOMAIN = input("\n Please enter the Portainer domain: ")

        # Input Grafana domain
        INPUT_GRAFANA_DOMAIN = input("\n Please enter the Grafana dashboards domain: ")

        # CREATE NGINX CONF
        create_nginx_conf(INPUT_API_DOMAIN,
                          INPUT_WEBSOCKET_DOMAIN,
                          INPUT_PORTAINER_DOMAIN,
                          INPUT_GRAFANA_DOMAIN
                          )
        # General variables
        RABBITMQ_HOST = "rabbitmq"
        # Vulnvision Variables
        VULNVISION_ALLOWED_HOSTS = INPUT_API_DOMAIN
        VULNVISION_DJANGO_DB_NAME = "vulnvision_database"
        VULNVISION_DJANGO_DB_USER = "vulnvision"
        VULNVISION_DJANGO_DB_PASSWORD = generate_random_password()
        VULNVISION_DJANGO_RABBITMQ_HOST = RABBITMQ_HOST
        VULNVISION_DJANGO_RABBITMQ_USER = "vulnvision"
        VULNVISION_DJANGO_RABBITMQ_PASSWORD = generate_random_password()
        VULNVISION_SECRET_KEY = generate_random_password()
        VULNVISION_DEBUG = False
        VULNVISION_ENV_CONTENT = f"""ALLOWED_HOSTS={VULNVISION_ALLOWED_HOSTS}
DJANGO_DB_NAME={VULNVISION_DJANGO_DB_NAME}
DJANGO_DB_USER={VULNVISION_DJANGO_DB_USER}
DJANGO_DB_PASSWORD={VULNVISION_DJANGO_DB_PASSWORD}
DJANGO_RABBITMQ_HOST={VULNVISION_DJANGO_RABBITMQ_HOST}
DJANGO_RABBITMQ_USER={VULNVISION_DJANGO_RABBITMQ_USER}
DJANGO_RABBITMQ_PASSWORD={VULNVISION_DJANGO_RABBITMQ_PASSWORD}
SECRET_KEY={VULNVISION_SECRET_KEY}
DEBUG={VULNVISION_DEBUG}
REDIS_IP_HOST=vulnvision_redis
POSTGRES_IP_HOST=vulnvision_postgres_db
CORS_ALLOWED_ORIGINS=http://127.0.0.1:3000,http://localhost:3000
        """
        VULNVISION_POSTGRES_ENV_CONTENT = postgres_env_content(VULNVISION_DJANGO_DB_NAME,
                                                               VULNVISION_DJANGO_DB_USER,
                                                               VULNVISION_DJANGO_DB_PASSWORD,
                                                               )
        VULNVISION_ENV_FILE = generate_folder_file(file_name="vulnvision.env", content=VULNVISION_ENV_CONTENT)
        VULNVISION_POSTGRES_ENV_FILE = generate_folder_file(file_name="vulnvision_postgres.env", content=VULNVISION_POSTGRES_ENV_CONTENT)

        # Nuclei Variables
        NUCLEI_DJANGO_DB_NAME = "nuclei_database"
        NUCLEI_DJANGO_DB_USER = "nuclei"
        NUCLEI_DJANGO_DB_PASSWORD = generate_random_password()
        NUCLEI_DJANGO_RABBITMQ_HOST = RABBITMQ_HOST
        NUCLEI_DJANGO_RABBITMQ_USER = "nuclei"
        NUCLEI_DJANGO_RABBITMQ_PASSWORD = generate_random_password()
        NUCLEI_ENV_CONTENT = microservice_env_content(NUCLEI_DJANGO_DB_NAME,
                                                      NUCLEI_DJANGO_DB_USER,
                                                      NUCLEI_DJANGO_DB_PASSWORD,
                                                      NUCLEI_DJANGO_RABBITMQ_HOST,
                                                      NUCLEI_DJANGO_RABBITMQ_USER,
                                                      NUCLEI_DJANGO_RABBITMQ_PASSWORD
                                                      )
        NUCLEI_POSTGRES_ENV_CONTENT = postgres_env_content(NUCLEI_DJANGO_DB_NAME,
                                                           NUCLEI_DJANGO_DB_USER,
                                                           NUCLEI_DJANGO_DB_PASSWORD,
                                                           )
        NUCLEI_ENV_FILE = generate_folder_file(file_name="nuclei.env", content=NUCLEI_ENV_CONTENT)
        NUCLEI_POSTGRES_ENV_FILE = generate_folder_file(file_name="nuclei_postgres.env", content=NUCLEI_POSTGRES_ENV_CONTENT)

        # Nmap Variables
        NMAP_DJANGO_DB_NAME = "nmap_database"
        NMAP_DJANGO_DB_USER = "nmap"
        NMAP_DJANGO_DB_PASSWORD = generate_random_password()
        NMAP_DJANGO_RABBITMQ_HOST = RABBITMQ_HOST
        NMAP_DJANGO_RABBITMQ_USER = "nmap"
        NMAP_DJANGO_RABBITMQ_PASSWORD = generate_random_password()
        NMAP_ENV_CONTENT = microservice_env_content(NMAP_DJANGO_DB_NAME,
                                                    NMAP_DJANGO_DB_USER,
                                                    NMAP_DJANGO_DB_PASSWORD,
                                                    NMAP_DJANGO_RABBITMQ_HOST,
                                                    NMAP_DJANGO_RABBITMQ_USER,
                                                    NMAP_DJANGO_RABBITMQ_PASSWORD
                                                    )
        NMAP_POSTGRES_ENV_CONTENT = postgres_env_content(NMAP_DJANGO_DB_NAME,
                                                        NMAP_DJANGO_DB_USER,
                                                        NMAP_DJANGO_DB_PASSWORD,
                                                        )
        NMAP_ENV_FILE = generate_folder_file(file_name="nmap.env", content=NMAP_ENV_CONTENT)
        NMAP_POSTGRES_ENV_FILE = generate_folder_file(file_name="nmap_postgres.env", content=NMAP_POSTGRES_ENV_CONTENT)

        # Grafana variables
        INPUT_GRAFANA_ADMIN_PASSWORD = "admin"
        GRAFANA_ENV_CONTENT = f"""GF_SECURITY_ADMIN_PASSWORD={INPUT_GRAFANA_ADMIN_PASSWORD}"""
        GRAFANA_ENV_FILE = generate_folder_file(file_name="grafana.env", content=GRAFANA_ENV_CONTENT)

        # create Rabbitmq env
        create_rabbitmq_env(VULNVISION_DJANGO_RABBITMQ_USER,
                            VULNVISION_DJANGO_RABBITMQ_PASSWORD,
                            NUCLEI_DJANGO_RABBITMQ_USER,
                            NUCLEI_DJANGO_RABBITMQ_PASSWORD,
                            NMAP_DJANGO_RABBITMQ_USER,
                            NMAP_DJANGO_RABBITMQ_PASSWORD,
                            )

        try:
            # install_os_dependencies_ubuntu()
            # docker swarm init
            # os.system("docker-compose up -d")
            os.system("docker-compose up")

        except Exception as e:
            print(e)
    elif answer.lower() == "n":
        break
    else:
        print("\n"  + "Please enter y or n." + "\n")
