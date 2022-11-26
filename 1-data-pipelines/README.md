# Data Pipelines

The following lists the steps taken to create the Data Pipeline using Airflow.

## Installation 

The following [documentation](https://airflow.apache.org/docs/apache-airflow/2.1.3/start/docker.html) is a simple setup guide for Airflow.

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

Next, we can declare required environment variables by creating an `.env` file
```bash
echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env
```

---

### Airflow

Run `airflow-init` image to create first user account on Airflow:
```bash
docker-compose up airflow-init
```

---
### Spark
Next, we can pip install PySpark for data-cleaning (to standardise current Spark version upon taking challenge)
```bash
pip install pyspark==3.3.1
```

---
### In overall
Subsequently, we can run all containers in Docker Compose with:
```bash
docker-compose up
```

----
## References
- [Airflow](https://airflow.apache.org/docs/apache-airflow/2.1.3/start/docker.html) 
- [Youtube](https://www.youtube.com/watch?v=aTaytcxy2Ck)

