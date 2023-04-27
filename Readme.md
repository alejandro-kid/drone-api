# Drone Api

Drone API is an exercise to evaluate programmer skills for the position of Software Engineer in MusalaSoft. The API was developed in Python using the framework Flask. The exercise was to check the candidate's abilities and not his proficiency in a specific programming language. For this reason, was chosen Python Flask and not NodeJS as suggested (at the end of the exercise document when said: "JUnit tests are optional..."), and the test framework Pytest.

## Build

To build the project you need to have installed [docker](https://docs.docker.com/engine/install/) and run the following command:

```bash
docker build -t drone-api .
```

or directly download the container from package repository of project in [github](https://github.com/alejandro-kid/drone-api/pkgs/container/drone-api)

## Run

To run the project you need to have installed [docker](https://docs.docker.com/engine/install/) and run the following command:

```bash
docker run -p 80:8000 drone-api
```

## Pay special attention

### Swagger OAS 3.0

The Api was creted using that bring us an UI to test the api, you can access to it putting in the end of the url the endpoint `/ui`

### Github Actions

The project has a github action to, test code,  build and publish the container in the package repository of project in [Drone-APi](https://github.com/alejandro-kid/drone-api/pkgs/container/drone-api)