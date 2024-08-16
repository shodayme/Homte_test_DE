## Homte_test_DE

### Project architecture
![](diagrams/project_architecture.png)
### Prerequisites
Docker

Docker Compose

Python
### Setup
#### Clone the Repository
```git clone https://github.com/shodayme/Homte_test_DE.git```

```
cd Homte_test_DE
```
#### build the docker images
```
docker compose build
```

### Usage
#### start the api and database container
```
docker compose up postgres_db api -d
```
#### run the etl
```
docker compose run -e INPUT_PATH=/relative/path/to/data/dir/ data_processor
```
### Testing
In order to run the unit tests locally, please perform the following steps under the project root directory:
1. setup the testing venv

```
python -m venv test_venv
```

```
source test_venv/bin/activate
```

```
pip install -r test_requirements.txt
```

3. run the following command:

```
pytest -v
```
### Cloud deployment architecture
![](diagrams/aws_diagram.png)
