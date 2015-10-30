# Docker: MunkiReport playground

* Use Docker Compose for running MySQL and [MunkiReport](https://github.com/munkireport/munkireport-php) containers and importing MySQL database
* Use Docker for building python:2.7 image with MySQL-python (1.2.5) module

**Requirements**

* Docker Toolbox (OS X)
* Docker Compose 1.5.0rc1 (should be included in the Toolbox in the future)

**Docker images @ Docker Hub**

* [Ubuntu](https://hub.docker.com/_/ubuntu/) (for data container)
* [MySQL](https://registry.hub.docker.com/_/mysql/)
* [Python](https://hub.docker.com/_/python/)
* [MunkiReport](https://registry.hub.docker.com/u/hunty1/munkireport-docker/)

## Preparations (optional)

Create separate local Docker Machine `dev` for testing:

`$ docker-machine create -d virtualbox dev`

`$ eval "$(docker-machine env dev)"`

`$ docker-machine ls`

Save Docker Machine IP address to environment variable:

`$ export DOCKER_MACHINE_IP=$(docker-machine ip dev)`

## Setup

Get this repo:

`$ git clone git@github.com:jlehikoinen/munkireport-playground.git`

`$ cd munkireport-playground`

## Run containers (3 different options)

Run MySQL and MunkiReport containers:

`$ docker-compose up -d`

Run MySQL containers and import MySQL database. Before running this option, rename your database dump to `db.sql` and place it  to the root of working dir:

`$ docker-compose -f docker-compose-import.yml up -d`

Run MySQL & MunkiReport containers and import MySQL database:

`$ docker-compose -f docker-compose-all.yml up -d`

## Build Python with MySQL-python module

Build `my_python` image with onbuild Python image (takes some time 1st time):

`$ docker build -t my_python build_python`

List images:

`$ docker images`

Run interactive shell in Python container:

`$ docker run -it --rm -v "$PWD"/code:/usr/src/app --link mysqlplayground_mysql_1:mysql my_python bash`

`# python example.py`

`# exit`

Run example script directly:

`$ docker run -it --rm -v "$PWD"/code:/usr/src/app --link mysqlplayground_mysql_1:mysql my_python python example.py`

## Run containers with separate docker commands

Create MySQL data container `db_data`:

`$ docker run -d -v /var/lib/mysql --name db_data ubuntu`

Run MySQL binary container `db_app`:

`$ docker run -d --name db_app --volumes-from db_data -p 3306:3306 -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=munkireport -e MYSQL_USER=admin -e MYSQL_PASSWORD=admin mysql`

Import MySQL database. Copy sql dump file to $PWD, replace `<my-db>.sql` with your db name and run a temp container:

`$ docker run -it --rm --link=db_app:mysql -v "$PWD":/tmp mysql sh -c 'exec mysql -h"$MYSQL_PORT_3306_TCP_ADDR" -P"$MYSQL_PORT_3306_TCP_PORT" -uroot -p"$MYSQL_ENV_MYSQL_ROOT_PASSWORD" "$MYSQL_ENV_MYSQL_DATABASE" < /tmp/<my-db>.sql'`

Run MunkiReport `mr` container and connect it to `db_app` container:

`$ docker run -d -p 80:80 --name mr --link db_app:mysql -e DB_NAME=munkireport -e DB_USER=admin -e DB_PASS=admin -e DB_SERVER=$DOCKER_MACHINE_IP -e MR_SITENAME="Local tests" hunty1/munkireport-docker`

Run interactive Python container:

`$ docker run -it --rm -v "$PWD"/code:/usr/src/app --link db_app:mysql my_python bash`

## After testing

Stop and delete all containers:

`$ docker stop $(docker ps -aq) && docker rm $(docker ps -aq)`

Stop Docker Machine `dev`:

`$ docker-machine stop dev`
