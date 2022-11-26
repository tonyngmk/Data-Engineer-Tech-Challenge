# Data Pipelines

The following lists the steps taken to create the Data Pipeline using Airflow.

## Installation 
### Spark
First, we can obtain PySpark conveniently through:
```bash
pip install pyspark==3.3.1
```

---
### Pipeline
Next, our hourly data-pipeline can be established with a simple `crontab -e` command:
```bash
0 * * * * python src/process_applications.py > logs/local_logs/$(date +"%Y_%m_%d_%I").log &
```

## Explanation
1. Files ingested would be placed into `data/input`, while processed files is stored at `data/output`.
    - To add simple deletion of all input files after processing if pipeline goes live to reduce storage space.

2. Data cleaning logic is solely handled by `src/process_applications.py` using PySpark, where application reads all relevant `.csv` files in folder.

3. We just need to create a simple cronjob to run the above Python script every hourly to fulfil pipeline requirement.
