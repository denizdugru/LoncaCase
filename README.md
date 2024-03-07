# Lonca Case Study

## Project overview
In this project main goal is to extract the data from sample XLM file and save as mongo document.

## Features
* **llm parser**: Added llm support for keyword correction and also xlm parser to the desired schema (experimental).
* **periodic task**: Added an XML parser without uvicorn app.
* **logging**: Added logger to track the processes and stdout support.
* **file upload**: Added support to upload files.
* **config**: Added new env file configurations to easily access variables, added new logic to convert variables to float.
* **mongo**: Integrated mongoengine (an Object-Document Mapper for MongoDB), implemented creation of the docs and other utilities..
* **pre_commit**: Added precommit config file, added .gitignore, black linted, hook for debug statements.
* **xml parser**: Added XML parser for single files to prevent duplication of  products and ensure only new products are populated.
* **xml folder parser**: Added XML parser for folders to prevent duplication of products and ensure only new files are extracted.

## Requirements
- The project has been created and tested on macOS M2 setup.
- Docker is required to run the MongoDB service and optionally, the FastAPI service in a containerized environment.
- Python 3.6 or higher is required to run the FastAPI service and the periodic extraction script.
- The following Python packages are required and can be installed using the provided requirements.txt file
- The provided .env.local and .env files contain environment variables required for the application. Ensure these files are present and properly configured before running the services.
- The token for the LLM feature is provided through the email, please don't share it or push it to your repository.

## Installation
1. Download [Docker](https://docs.docker.com/get-docker/) and ensure it's set up properly
2. Clone the repository:
```bash
git clone <repository_url>
```
3. If you want to run the service locally, create a virtual environment with the following command:
```bash
python3 -m venv <your_env_file>
```

Activate the virtual environment and install the requirements:
```bash
source <your_env_file>/bin/activate
pip install -r reqs/requirements.txt
```

Note: Check the [documentation](https://docs.python.org/3/library/venv.html) for other operating systems.

## Usage
There are three different methods and usages.


### Running the service locally

After creating the virtual environment and installing the requirements, start the service with the following command:
```bash
set -a; source .env.local; set +a; python main.py
```
- The service will start on your local host machine. Visit "http://localhost:8000/docs#/" in any browser to use the endpoints.
- The .env.local and .env files are available in the repository since it's a case study and doesn't contain important credentials or secrets.
- The periodic event that listens to the assets folder starts on "startup" event and runs every 60 minutes.
- Ensure the MongoDB Docker is running:

```bash
docker ps
```


### Running the Service in Docker Mode

1. To start the Docker containers, run:
```bash
docker-compose up -d
```
2. After a short period, the "app_container" and "mongo_container" will be in the running state. To check, use the command:

```bash
docker ps
```


### Running the Periodic Task without FastAPI

1. Another way to start the periodic extraction without Docker and the service is to run the "periodic_task.py" file. It uses the same extraction and listening logic but uses the schedule module to run the task:

```bash
set -a; source .env.local; set +a; python periodic_task.py
```
2. There will be a log on your console indicating that the periodic task is scheduled.

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
