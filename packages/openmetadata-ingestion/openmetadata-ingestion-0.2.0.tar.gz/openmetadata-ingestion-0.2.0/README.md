---
This guide will help you setup the Ingestion framework and connectors
---

![Python version 3.8+](https://img.shields.io/badge/python-3.8%2B-blue)

# Setup Ingestion

Ingestion is a data ingestion library, which is inspired by [Apache Gobblin](https://gobblin.apache.org/). It could be
used in an orchestration framework\(e.g. Apache Airflow\) to build data for OpenMetadata.
**Prerequisites**

- Python &gt;= 3.8.x

### Install From PyPI

```text
python3 -m pip install --upgrade pip wheel setuptools
python3 -m pip install --upgrade openmetadata-ingestion
python3 -m spacy download en_core_web_sm
```

### Install Ingestion Connector Dependencies

**Sources:**

| Plugin Name     | Install Command                                         | Provides        |
| --------------- | ------------------------------------------------------- | --------------- |
| athena          | `pip install 'openmetadata-ingestion[athena]'`          | AWS Athena      |
| bigquery        | `pip install 'openmetadata-ingestion[bigquery]'`        | BigQuery        |
| bigquery-usage  | `pip install 'openmetadata-ingestion[bigquery-usage]'`  | BigQuery usage  |
| hive            | `pip install 'openmetadata-ingestion[hive]'`            | Hive            |
| ldap-users      | `pip install 'openmetadata-ingestion[ldap-users]'`      | LDAP            |
| mssql           | `pip install 'openmetadata-ingestion[mssql]'`           | SQL Server      |
| mssql-odbc      | `pip install 'openmetadata-ingestion[mssql-odbc]'`      | SQL Server ODBC |
| mysql           | `pip install 'openmetadata-ingestion[mysql]'`           | MySQL           |
| oracle          | `pip install 'openmetadata-ingestion[oracle]'`          | Oracle          |
| postgres        | `pip install 'openmetadata-ingestion[postgres]'`        | Postgres        |
| redshift        | `pip install 'openmetadata-ingestion[redshift]'`        | Redshift        |
| redshift-usage  | `pip install 'openmetadata-ingestion[redshift-usage]'`  | Redshift Usage  |
| snowflake       | `pip install 'openmetadata-ingestion[snowflake]'`       | Snowflake       |
| snowflake-usage | `pip install 'openmetadata-ingestion[snowflake-usage]'` | Snowflake usage |
| elasticsearch   | `pip install 'openmetadata-ingestion[elasticsearch]'`   | Elastic Search  |
| sample-tables   | `pip install 'openmetadata-ingestion[sample-tables]'`   | Sample Tables   |

#### Generate Redshift Data

```text
metadata ingest -c ./pipelines/redshift.json
```

#### Generate Redshift Usage Data

```text
metadata ingest -c ./pipelines/redshift_usage.json
```

#### Generate Sample Tables

```text
metadata ingest -c ./pipelines/sample_tables.json
```

#### Generate Sample Users

```text
metadata ingest -c ./pipelines/sample_users.json
```

#### Ingest MySQL data to Metadata APIs

```text
metadata ingest -c ./pipelines/mysql.json
```

#### Ingest Bigquery data to Metadata APIs

```text
export GOOGLE_APPLICATION_CREDENTIALS="$PWD/pipelines/creds/bigquery-cred.json"
metadata ingest -c ./pipelines/bigquery.json
```

#### Index Metadata into ElasticSearch

#### Run ElasticSearch docker

```text
docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.10.2
```

#### Run ingestion connector

```text
metadata ingest -c ./pipelines/metadata_to_es.json
```
