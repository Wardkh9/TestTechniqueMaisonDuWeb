# Projet d'automatisation de tests avec Selenium + Docker

## Prérequis
- Docker et Docker Compose installés.

## Construction et lancement
```bash
docker-compose up --build

## Lancer uniquement les tests

##Lancement du projet docker
docker-compose up --build
Cela :

Crée un conteneur Selenium Hub

Lance un nœud Chrome

Construit l’image de test (avec Python + Selenium)

Exécute test_script.py qui se connecte à Selenium Grid