# Development Environment

## Install Docker

First, you need to have Docker and Docker Compose installed on your system. 

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Environment variables

Create a `.env` file to the root of the repository and write needed environment variables to it. 

[Example .env](./.env.example)

[Environment variable docs](./environment_variables.md)

## Running the environment

To start the environment, you have to run this command in the root the repository. 
```
docker-compose up -d --build
```
Now if you go to [localhost:8000](localhost:8000), you should see the RNames app running. You can also go to [localhost:8001](localhost:8001) to see or modify the created database. 

To see logs you can run this command. You can also specify a container if you only want to see specific logs `docker-compose logs <container> -f`. 
```
docker-compose logs -f
```
If you want to shutdown the containers, you can run this command. 
```
docker-compose down
```
In the case of wanting to also remove the volumes (meaning that the database will be reset), you can run `docker-compose down -v`.

### Other useful commands

You can execute commands inside the container by running:
```
docker-compose exec <container> <command>
```
For example, if you need to make migrations inside django, you can run `docker-compose exec web python manage.py makemigrations`. Then to migrate the database you can run `docker-compose exec web python manage.py migrate`. These commands should usually been run when the developer has made changes to the models or created a new app inside django. See more in [Django docs](https://docs.djangoproject.com/en/3.2/).

Please note, that currently the django application makes migrations and migrates the database every time the django container is started. If this proves to be cumbersome the lines can be commented out in [entrypoint.sh](./../app/scripts/entrypoint.sh).
