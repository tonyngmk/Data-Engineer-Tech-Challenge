# Data Pipelines

The following lists the steps taken to create the Data Pipeline using Airflow.

## Installation 

Use the following [documentation](https://airflow.apache.org/docs/apache-airflow/2.1.3/start/docker.html) as a quick setup guide for Airflow.

Firstly, curl `docker-compose.yaml` to deploy on docker compose.
```bash
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.1.3/docker-compose.yaml'
```

Thereafter, create required folders to setup data pipeline.
```bash
mkdir ./logs ./dags ./plugins
```
- Logs: Store logs
- Plugins: Contains plugins
- Dags: Store DAGs created

Next, we can store environment variables by creating an `.env` file
```bash
echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env
```

---

Next, we can start deploying Airflow on Docker Compose by creating a first user account with:
```bash
docker-compose up airflow-init
```

Subsequently, we can run all containers in Docker Compose with:
```bash
docker-compose up
```


## References
- [Airflow](https://airflow.apache.org/docs/apache-airflow/2.1.3/start/docker.html) 
- [Youtube](https://www.youtube.com/watch?v=aTaytcxy2Ck
)