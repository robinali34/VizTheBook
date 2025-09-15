# VizTheBook
The main objective of undertaking this project is to build an automated software system with visualizations that can aid in finding, filtering and searching through books on a given topic without having to read them first. 

## Pre-requisites
* docker
* docker-compose
* awscli

### Note for Windows Users
We highly recommend using Cygwin on Windows to get a Linux-like terminal environment. This project makes use of a Makefile and this dependency should be installed in the Cygwin terminal. For instructions on installation, see these: https://wiki.usask.ca/display/MESH/Running+Python+from+the+Cygwin+Terminal. The suggested section is `Configuring Cygwin`.

### Installing docker/docker-compose
To install docker, please follow the instructions for your operating system: https://docs.docker.com/get-docker/</br>
To install docker-compose, follow the instructions for your operating system: https://docs.docker.com/compose/install/</br>

These combined dependencies will build and run our whole application.

### Installing awscli
A `Makefile` has been provided in the root of the project directory. Run `make install-deps` to install the awscli dependency. This dependency will be used to load data into the MongoDB container created.

## Running the Project.
From the root project directory, run `make run`. The application will then be accesible from your browser: `http://localhost:5000`

This command will build the two docker containers required to run the application and load the demo data for the application.

## Cleaning the Project
If you want to shutdown the application and clean up, run `make clean`.

This command will stop the current running docker containers and remove the sample data.

## Local Development
We understand that docker containers may not be the best approach for quickly testing changes in a development mode. 

To develop locally, you can run `make database` to run the local MongoDB container. You can take the `requirements.txt` and install that into a local python virtual environment and then run `python app.py`. This local mode will be faster for testing changes.

## Contributing
We appreciate any and all contributions to our project. As far as actually contributing, we recommend forking the repository and making changes against your local fork. Please open a PR from your fork against our master branch.
