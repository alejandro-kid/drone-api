# Drone Api

Drone API is an exercise to evaluate programmer skills for the position of Software Engineer in MusalaSoft. The API was developed in Python using the framework Flask. The exercise was to check the candidate's abilities and not his proficiency in a specific programming language. For this reason, Python Flask was chosen and not NodeJS as suggested (at the end of the exercise document when it said: "JUnit tests are optional..."), and the test framework Pytest.

## Build

To build the project you need to have installed [docker](https://docs.docker.com/engine/install/) and run the following command:

```bash
docker build -t drone-api .
```

or directly download the container from the package repository of the project in [github](https://github.com/alejandro-kid/drone-api/pkgs/container/drone-api)

## Run

To run the project you need to have installed [docker](https://docs.docker.com/engine/install/) and run the following command:

```bash
docker run -p 80:8000 drone-api
```

## Pay special attention

### What I did

All needed endpoints and exercise endpoints are not in the code.

### Init DB

The first thing you need to do is activate the endpoint: /create_db. This endpoint creates the Schema Model of DB. After that, you can activate any endpoint of the API.

### Swagger OAS 3.0

The API was created using Connection, a framework that uses Swagger OAS3.0 to configure and develop APIs, bring us a UI to test the API, you can access it by putting at the end of the URL the endpoint `/ui`

### Github Actions

The project has a GitHub action to, test code,  build and publish the container in the package repository of the project in [Drone-APi](https://github.com/alejandro-kid/drone-api/pkgs/container/drone-api)

### Test

The project has a group of tests, unit tests, and integration tests. The author uses many techniques to test the code, for example, the library Hypothesis of Python that generate a lot of data for test automatically.

### Class Implementation

Drone is the main class of all business logic, have the method of adding medications for example with a simple algorithm that checks the weight of the drone and the weight of the medication, if the weight of the medication is less than the weight of the drone, the medication is added to the drone.

In Medicine class, the image attribute is not necessary to store, here we use the strategy of storing de image physically in a folder and the name of it is the name of the medicine, for this reason, the author aggregated a restriction of a unique name for medicine.
> Note: the author knows that we can use the same name of a medicine but with a different code and the same image for the same medicine, but this context is not necessary for this exercise (I think).

Validation is in data of both classes, the author implements many validations schema for different purpose, and validate the constraints with Regular expressions.
