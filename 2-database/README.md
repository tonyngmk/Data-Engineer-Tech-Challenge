# Data Pipelines

The following lists the steps taken to create the Data Pipeline using Airflow.

## Installation 
### Postgresql
First, we can copy the `docker-compose.yaml` file in provided [link](https://hub.docker.com/_/postgres) and run:
```bash
docker-compose up
```
---

## ERD
```mermaid
erDiagram
    MEMBER ||--o{ TRANSACTION : places
    MEMBER {
        string membership_id
        string name
        string first_name
        string last_name
        string email
        int    date_of_birth
        string sha256_dob
        int    mobile_no
    }
    TRANSACTION ||--|{ ITEM : contains
    TRANSACTION {
        int   transaction_id
        int   membership_id
        int   item_id
    }
    ITEM {
        int    item_id
        string item_name
        string manufacturer_name
        float  cost
        float  weight_kg
    }
```
