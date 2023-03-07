## Summary

Orange County Lettings website

## Local Development

### Prerequisites

- GitHub account with read access to this repository
- Git CLI
- SQLite3 CLI
- Python interpreter, version 3.6 or higher

In the rest of the local development documentation, it is assumed that the `python` command in your shell OS runs the above Python interpreter (unless a virtual environment is enabled).

### macOS / Linux

#### Clone the repository

- cd /path/to/put/project/in
- git clone https://github.com/OpenClassrooms-Student-Center/Python-OC-Lettings-FR.git

#### Create the virtual environment

- `cd /path/to/Python-OC-Lettings-FR`
- `python -m venv`
- `apt-get install python3-venv` (If the previous step has errors with a package not found on Ubuntu)
- Activate the `source venv/bin/activate` environment
- Confirm that the `python` command runs the Python interpreter in the virtual environment
which python` command
- Confirm that the version of the Python interpreter is version 3.6 or higher `python --version`
- Confirm that the `pip` command runs the pip executable in the virtual environment, `which pip`
- To disable the environment, `deactivate`

#### Run the site

- `cd /path/to/Python-OC-Lettings-FR`
- source venv/bin/activate`
- `pip install --requirement requirements.txt`
- python manage.py runserver`
- Go to `http://localhost:8000` in a browser.
- Confirm that the site is working and that it is possible to navigate (you should see several profiles and locations).

#### Linting

- cd /path/to/Python-OC-Lettings-FR
- source venv/bin/activate`
- `flake8`

#### Unit testing

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `pytest`

#### Database

- `cd /path/to/Python-OC-Lettings-FR`
- Open a shell session `sqlite3`
- Connect to the database `.open oc-lettings-site.sqlite3`
- Display the tables in the database `.tables`
- Display the columns in the profiles table, `pragma table_info(Python-OC-Lettings-FR_profile);`
- Run a query on the profiles table, `select user_id, favorite_city from
  Python-OC-Lettings-FR_profile where favorite_city like 'B%';`
- `.quit` to exit

#### Administration panel

- Go to `http://localhost:8000/admin`
- Log in with user `admin`, password `Abc1234!`

### Windows

Using PowerShell, as above except :

- To enable the virtual environment, `.\venv\Scripts\Activate.ps1` 
- Replace `which <my-command>` with `(Get-Command <my-command>).Path`

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