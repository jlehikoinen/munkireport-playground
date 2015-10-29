# Docker: Python & MySQL playground

Docker Python playground for testing ([MunkiReport](https://github.com/munkireport/munkireport-php)) MySQL queries.

* Docker builds python:2.7 image with MySQL-python (1.2.5) module
* Docker Compose is used for running MySQL containers

**Requirements**

* Docker Toolbox

**Docker images @ Docker Hub**

* [Ubuntu](https://hub.docker.com/_/ubuntu/) (for data container)
* [MySQL](https://registry.hub.docker.com/_/mysql/)
* [Python](https://hub.docker.com/_/python/)

## Preparations (optional)

Create separate local Docker Machine `dev` for testing:

`$ docker-machine create -d virtualbox dev`

`$ eval "$(docker-machine env dev)"`

`$ docker-machine ls`

## Setup

Get this repo:

`$ git clone git@github.com:jlehikoinen/mysql-playground.git`

`$ cd mysql-playground`

Build `my_python` image with onbuild Python image (takes some time 1st time):

`$ docker build -t my_python build_python`

List images:

`$ docker images`

## Run containers

Run MySQL containers:

`$ docker-compose up -d`

Import database. Copy sql dump file to $PWD, replace `<my-db>.sql` with your db name and run a temp container:

```
$ docker run --rm \
		   --link=mysqlplayground_mysql_1:mysql \
		   -v "$PWD":/tmp mysql \
		   sh -c 'exec mysql \
		   -h"$MYSQL_PORT_3306_TCP_ADDR" \
		   -P"$MYSQL_PORT_3306_TCP_PORT" \
		   -uroot \
		   -p"$MYSQL_ENV_MYSQL_ROOT_PASSWORD" \
		   "$MYSQL_ENV_MYSQL_DATABASE" \
		   < /tmp/<my-db>.sql'
```

Run interactive shell in Python container:

`$ docker run -it --rm -v "$PWD"/code:/usr/src/app --link mysqlplayground_mysql_1:mysql my_python bash`

`# python example.py`

`# exit`

Run example script directly:

`$ docker run -it --rm -v "$PWD"/code:/usr/src/app --link mysqlplayground_mysql_1:mysql my_python python example.py`

## Run containers with separate docker commands

`$ docker run -d -v /var/lib/mysql --name db_data ubuntu`

`$ docker run -d --name db_app --volumes-from db_data -p 3306:3306 -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=munkireport -e MYSQL_USER=admin -e MYSQL_PASSWORD=admin mysql`

`$ docker run -it --rm --link=db_app:mysql -v "$PWD":/tmp mysql sh -c 'exec mysql -h"$MYSQL_PORT_3306_TCP_ADDR" -P"$MYSQL_PORT_3306_TCP_PORT" -uroot -p"$MYSQL_ENV_MYSQL_ROOT_PASSWORD" "$MYSQL_ENV_MYSQL_DATABASE" < /tmp/<my-db>.sql'`

`$ docker run -it --rm -v "$PWD"/code:/usr/src/app --link db_app:mysql my_python bash`

## After testing

Stop and delete all containers:

`$ docker stop $(docker ps -aq) && docker rm $(docker ps -aq)`

Delete `my_python` image (optional):

`$ docker rmi my_python`
