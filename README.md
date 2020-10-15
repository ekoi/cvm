# Docker with pre-defined Dataverse cvm-autocomplete module 
This module is developed to run Dataverse with pre-defined setting and CESSDA Metadata.

##### Prerequisites 
Before running the Dataverse on Docker, we need install some of the other stuff. 
On Mac OS X, we’ll use [brew](https://brew.sh/) and the following softwares:
* Git: `brew install git`.
* Docker: `brew cask install docker`
* Docker-compose: `brew cask install docker-compose`

#### Versions
The table below gives the preferred versions. 

 Requirement            | Version
------------------------|--------
Git                     | 2.26.2
Docker                  | 19.03.12
Docker-compose          | 1.26.2

## Installation

`git clone https://github.com/ekoi/speeltuin.git`

`cd speeltuin/docker`

## Start Dataverse for the first time
`docker-compose up -d`

Wait for some minutes. 
To find out if the application is ready, check the dataverse log:
`docker log -f dataverse` 
The Dataverse is ready when the following line is showed in the dataverse log:

`Found Storage Driver: local for Local`

Navigate to [http://localhost:8080/](http://localhost:8080/) in your browser.
username: dataverseAdmin
password: admin

## Stop Dataverse
`docker-compose down`

## Remove installation
```
docker-compose down
docker volume prune
```
## Start Dataverse
`docker-compose start`

## Re-install Dataverse
```
docker-compose down
docker volume prune
git pull origin master
docker-compose up --force-recreate
```

