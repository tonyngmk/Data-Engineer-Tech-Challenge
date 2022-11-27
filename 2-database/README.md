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
        text       membership_id PK
        text       name
        text       first_name
        text       last_name
        text       email
        integer    date_of_birth
        text       sha256_dob
        integer    mobile_no
    }
    TRANSACTION ||--|{ ITEM : contains
    TRANSACTION {
        integer    transaction_id PK
        integer    membership_id  FK
        integer    item_id        FK
    }
    ITEM {
        integer    item_id        PK
        text       item_name
        text       manufacturer_name
        real       cost
        real       weight_kg
    }
```
