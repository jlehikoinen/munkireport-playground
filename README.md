# Docker - Python & MySQL playground

- Dockerfile builds python:2.7 image with MySQL-python (1.2.5)
- Docker Compose is used for running MySQL containers

## Pre-requisites

- Docker Toolbox

## Preparations

Create separate local Docker Machine `dev` for testing:

`$ docker-machine create -d virtualbox dev`

`$ eval "$(docker-machine env dev)"`

`$ docker-machine ls`

Deliver Docker Machine (`dev`) IP address to container via environment variable:

`$ export DOCKER_MACHINE_IP=$(docker-machine ip dev)`

This host IP address will be used in the examples:

```
192.168.99.100
```

## Setup

Get this repo:

`$ git clone git@github.com:jlehikoinen/mysql-playground.git`

`$ cd mysql-playground`

Build `my_python` image with onbuild Python image (takes some time 1st time):

`$ docker build -t my_python python_build`

Run MySQL containers:

`$ docker-compose up -d`

Import database. Copy sql dump file to this folder and run a temp container:

`$ docker run -it --rm --link=mysqlplayground_mysql_1:mysql -v "$PWD":/tmp/ mysql sh -c 'exec mysql -h192.168.99.100 -P3306 -uroot -proot munkireport < /tmp/<my-db>.sql'`

Run interactive Python container:

`$ docker run -it --rm -v "$PWD"/code:/usr/src/app --link mysqlplayground_mysql_1:mysql -e HOST_IP=$DOCKER_MACHINE_IP my_python bash`

Run example Python script directly:

`$ docker run -it --rm -v "$PWD"/code:/usr/src/app --link mysqlplayground_mysql_1:mysql -e HOST_IP=$DOCKER_MACHINE_IP my_python python example.py`

## Running containers with separate docker commands

`$ docker run -d -v /var/lib/mysql --name db_data ubuntu`

`$ docker run -d --name db_app --volumes-from db_data -p 3306:3306 -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=munkireport -e MYSQL_USER=admin -e MYSQL_PASSWORD=admin mysql`

`$ docker run -it --rm --link=db_app:mysql -v "$PWD":/tmp/ mysql sh -c 'exec mysql -h192.168.99.100 -P3306 -uroot -proot munkireport < /tmp/<munkireport-db>.sql'`

`$ docker run -it --rm -v "$PWD"/code:/code --link db_app:mysql -e HOST_IP=$DOCKER_MACHINE_IP my_python bash`

## After testing

Stop and delete all containers:

`$ docker stop $(docker ps -aq) && docker rm $(docker ps -aq)`

Delete `my_python` image:

`$ docker rmi my_python`