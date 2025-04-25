# Étape de base : image Ubuntu
FROM ubuntu:22.04

# Installer Python, pip et autres utilitaires
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    curl \
    unzip \
    && apt-get clean

# Installer les librairies Python nécessaires
COPY requirements.txt /app/requirements.txt
RUN pip3 install --upgrade pip && pip3 install -r /app/requirements.txt

# Copier les scripts dans le conteneur
COPY . /app
WORKDIR /app

# Commande d’exécution des tests
CMD ["python3", "test_script.py"]docker-compose up --build