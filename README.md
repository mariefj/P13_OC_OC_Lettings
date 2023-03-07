## Résumé

Site web d'Orange County Lettings

## Développement local

### Prérequis

- Compte GitHub avec accès en lecture à ce repository
- Git CLI
- SQLite3 CLI
- Interpréteur Python, version 3.6 ou supérieure

Dans le reste de la documentation sur le développement local, il est supposé que la commande `python` de votre OS shell exécute l'interpréteur Python ci-dessus (à moins qu'un environnement virtuel ne soit activé).

### macOS / Linux

#### Cloner le repository

- `cd /path/to/put/project/in`
- `git clone https://github.com/OpenClassrooms-Student-Center/Python-OC-Lettings-FR.git`

#### Créer l'environnement virtuel

- `cd /path/to/Python-OC-Lettings-FR`
- `python -m venv venv`
- `apt-get install python3-venv` (Si l'étape précédente comporte des erreurs avec un paquet non trouvé sur Ubuntu)
- Activer l'environnement `source venv/bin/activate`
- Confirmer que la commande `python` exécute l'interpréteur Python dans l'environnement virtuel
`which python`
- Confirmer que la version de l'interpréteur Python est la version 3.6 ou supérieure `python --version`
- Confirmer que la commande `pip` exécute l'exécutable pip dans l'environnement virtuel, `which pip`
- Pour désactiver l'environnement, `deactivate`

#### Exécuter le site

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `pip install --requirement requirements.txt`
- `python manage.py runserver`
- Aller sur `http://localhost:8000` dans un navigateur.
- Confirmer que le site fonctionne et qu'il est possible de naviguer (vous devriez voir plusieurs profils et locations).

#### Linting

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `flake8`

#### Tests unitaires

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `pytest`

#### Base de données

- `cd /path/to/Python-OC-Lettings-FR`
- Ouvrir une session shell `sqlite3`
- Se connecter à la base de données `.open oc-lettings-site.sqlite3`
- Afficher les tables dans la base de données `.tables`
- Afficher les colonnes dans le tableau des profils, `pragma table_info(Python-OC-Lettings-FR_profile);`
- Lancer une requête sur la table des profils, `select user_id, favorite_city from
  Python-OC-Lettings-FR_profile where favorite_city like 'B%';`
- `.quit` pour quitter

#### Panel d'administration

- Aller sur `http://localhost:8000/admin`
- Connectez-vous avec l'utilisateur `admin`, mot de passe `Abc1234!`

### Windows

Utilisation de PowerShell, comme ci-dessus sauf :

- Pour activer l'environnement virtuel, `.\venv\Scripts\Activate.ps1` 
- Remplacer `which <my-command>` par `(Get-Command <my-command>).Path`

## CI/CD - CircleCI, Docker, DigitalOcean

### Setup

- First you need to create an account (if not already done) for CircleCI, Docker, Sentry and DigitalOcean.

- Follow this quickstart guide for CircleCI to install yout project : https://circleci.com/docs/getting-started/ (choose to use your .circleci/config.yml file)
- Create a new registry on DockerHub named oc-lettings (you can choose an other name but make sur you change every occurrences needed in config.yml)

- Then you can go into the project settings and add some environment variables : 

| Name                | Value |
|---                  |---|
| DOCKERHUB_USERNAME  | Name of Docker user  |
| DOCKERHUB_PASSWORD  | Password of Docker user  |
| ENV                 | PRODUCTION  |
| SECRET_KEY          | Django secret key, to use in settings, it's here registered as an environment variable so you'll have to create one with the following command `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`  |
| SENTRY_DSN          | Client key you can find in Project settings then Client keys on Sentry  |

### Containerisation

- Install Docker if not already installed

- If you want to test locally :
- If you are not in the repository :
- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`

- Create an image :
- `docker build -t oc-lettings:test .`
- Then add some environment variables in venv/bin/activate file (you can choose other ways to manage environment variables, here is one choice):
- ENV, SECRET_KEY, SENTRY_DSN (same values of the CircleCI environment variables set above) and SSH_HOST, you can set it at '0.0.0.0'
- `docker run --env ENV --env SECRET_KEY --env SENTRY_DSN --env SSH_HOST --name oc-lettings -d -p 8000:8000 oc-lettings:test`

- If you don't change the Dockerfile, the address where you'll find the site is http://0.0.0.0:8000/

- Also, if you want, you can go to this address : https://hub.docker.com/r/mariefj/oc-lettings/tags and pull the last image, then run it.

- To remove the container and the image, use the `docker rm $NAME_CONTAINER` and `docker rmi $NAME_IMAGE` (replace the names)

### Deploy

Here the app is deployed on a DigitalOcean's droplet on every push of the main branch (if the pipeline doesn't fail).
The site is located at this address : http://164.90.183.42:8000/

- To deploy it on a new droplet :
- Go on DigitalOcean and create droplet, you are free to choose the region, the size, the cpu options, for the image choose the Docker 20.10.21 on Ubuntu 22.04, for the authentication method choose SSH key (then follow the instructions), and add an hostname, for example oc-lettings

- Return on CircleCI, go into the project settings and add some environment variables : 

| Name                | Value |
|---                  |---|
| SSH_HOST  | Public IP address of your droplet  |
| SSH_USER  | root  |
- Add the ssh private key to CircleCI SSH keys of the project (if you followed the instructions with the same name and location, you get it with `cat ~/.ssh/id_rsa`)

- Setup the server, you'll just have to add some environment variables (again several ways exist to manage them, feel free to adapt if you have a prefered one and modify tne config.yml) :
- First you'll need to update the sshd_config to enable PermitUserEnvironment :
- `nano /etc/ssh/sshd_config`
- Modify to 'yes' the PermitUserEnvironment option
- `systemctl restart sshd_config` to update the environment

- And add the variables ENV, SECRET_KEY, SENTRY_DSN, SSH_HOST, with the same value as in CircleCi, make the command:
- `$NAME_ENV_VAR=$VALUE_ENV_VAR`, for example : `ENV=PRODUCTION`

- You're ready to launch the pipeline to deploy the app ! (you'll access the site at http://[ip_server]:8000)