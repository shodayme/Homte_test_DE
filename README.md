## Homte_test_DE

### Prerequisites
Docker
Docker Compose
### Usage
#### Clone the Repository
```git clone https://github.com/shodayme/Homte_test_DE.git```
```cd Homte_test_DE```
#### build the docker images

```docker compose build```

#### start the api and database container
```docker compose up postgres_db api -d```
#### run the etl
```docker compose run -e INPUT_PATH=/relative/path/to/data/dir/ data_processor```
