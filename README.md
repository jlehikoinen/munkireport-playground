# Docker: MunkiReport playground

* Docker Compose example of running MySQL and [MunkiReport](https://github.com/munkireport/munkireport-php) containers and importing MySQL database
* Docker for building python:2.7 image with MySQL-python (1.2.5) module

**Requirements**

* Docker Toolbox (OS X)

**Docker images @ Docker Hub**

* [Ubuntu](https://hub.docker.com/_/ubuntu/) (for data container)
* [MySQL](https://registry.hub.docker.com/_/mysql/)
* [Python](https://hub.docker.com/_/python/)
* [MunkiReport](https://registry.hub.docker.com/u/hunty1/munkireport-docker/)

## Preparations

Start local `default` Docker Machine:

`$ docker-machine start default`

`$ eval "$(docker-machine env default)"`

`$ docker-machine ls`

## Setup

Get this repo:

`$ git clone https://github.com/jlehikoinen/munkireport-playground.git`

`$ cd munkireport-playground`

## Additional information

Get Docker Machine `default` IP address:

`$ docker-machine ip default`

MunkiReport GUI credentials:

Username: `root`

Password: `root`

## Run containers (3 different options)

First check yaml file contents and edit them if needed.

Run MySQL and MunkiReport containers:

`$ docker-compose up -d`

Run MySQL containers and import MySQL database. Before running this option, rename your database dump to `db.sql` and place it  to the root of working dir:

`$ docker-compose -f docker-compose-import.yml up -d`

Run MySQL & MunkiReport containers and import MySQL database:

`$ docker-compose -f docker-compose-all.yml up -d`

Open MunkiReport GUI:

`$ open http://$(docker-machine ip default)`

## Custom configurations

Copy the `munkireport` folder from MunkiReport container to the root of working dir:

`$ docker cp munkireportplayground_mr_1:/www/munkireport .`

Stop & delete current MunkiReport container:

`$ docker stop munkireportplayground_mr_1`

`$ docker rm -f munkireportplayground_mr_1`

Run Docker Compose again which mounts `munkireport` host folder as a data volume:

`$ docker-compose -f docker-compose-custom-config.yml up -d`

Edit files in your local `munkireport` folder.

Refresh MunkiReport web GUI and login again.

## Build Python with MySQL-python module

Build `my_python` image with onbuild Python image (takes some time 1st time):

`$ docker build -t my_python build_python`

List images:

`$ docker images`

Run interactive shell in Python container:

`$ docker run -it --rm -v "$PWD"/code:/usr/src/app --link munkireportplayground_mysql_1:mysql my_python bash`

`# python example.py`

`# exit`

Run example script directly:

`$ docker run -it --rm -v "$PWD"/code:/usr/src/app --link munkireportplayground_mysql_1:mysql my_python python example.py`

## Run containers with separate docker commands

Create MySQL data container `db_data`:

`$ docker run -d -v /var/lib/mysql --name db_data ubuntu`

Run MySQL binary container `db_app`:

`$ docker run -d --name db_app --volumes-from db_data -p 3306:3306 -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=munkireport -e MYSQL_USER=admin -e MYSQL_PASSWORD=admin mysql`

Import MySQL database. Copy sql dump file to $PWD, replace `<my-db>.sql` with your db name and run a temp container:

`$ docker run -it --rm --link=db_app:mysql -v "$PWD":/tmp mysql sh -c 'exec mysql -h"$MYSQL_PORT_3306_TCP_ADDR" -P"$MYSQL_PORT_3306_TCP_PORT" -uroot -p"$MYSQL_ENV_MYSQL_ROOT_PASSWORD" "$MYSQL_ENV_MYSQL_DATABASE" < /tmp/<my-db>.sql'`

Run MunkiReport `mr` container and connect it to `db_app` container:

`$ docker run -d -p 80:80 --name mr --link db_app:mysql -e DB_NAME=munkireport -e DB_USER=admin -e DB_PASS=admin -e DB_SERVER=db_app -e MR_SITENAME="Local tests" hunty1/munkireport-docker`

Run MunkiReport container and mount host folder `munkireport` as a data volume:

`$ docker run -d -p 80:80 --name mr --link db_app:mysql -v "$PWD"/munkireport:/www/munkireport -e DB_NAME=munkireport -e DB_USER=admin -e DB_PASS=admin -e DB_SERVER=db_app -e MR_SITENAME="Local tests" hunty1/munkireport-docker`

Run interactive Python container:

`$ docker run -it --rm -v "$PWD"/code:/usr/src/app --link db_app:mysql my_python bash`

## After testing

Stop and delete all containers:

`$ docker stop $(docker ps -aq) && docker rm $(docker ps -aq)`

Stop Docker Machine `default`:

`$ docker-machine stop default`
