# DataTrust | Data Quality & Observability SaaS

An end-to-end analytics engineering portfolio project demonstrating data quality monitoring and pipeline reliability using Snowflake, dbt, Apache Airflow, and Tableau.

## Project Overview

DataTrust is a fictional SaaS platform designed to help organizations monitor data quality, identify failing data assets, and evaluate analytics pipeline reliability.

The project demonstrates an end-to-end analytics workflow, from data modeling and testing to orchestration and dashboard-based monitoring.

### Business Objectives

- Monitor data quality across customers, assets, and quality dimensions.
- Identify assets with high numbers of failed quality checks.
- Measure data quality pass rates.
- Track pipeline success rates and execution duration.
- Orchestrate transformation workflows using Apache Airflow.
- Present operational metrics through Tableau dashboards.

## Technology Stack

| Technology | Purpose |
|---|---|
| Snowflake | Cloud data warehouse |
| dbt Core | SQL transformations, data modeling, and testing |
| Apache Airflow | Workflow orchestration |
| Tableau | Data quality and pipeline monitoring dashboards |
| Python | Supporting development and orchestration |
| Docker Compose | Local Airflow environment |
| Git and GitHub | Version control and project documentation |

## Architecture

The project follows a layered analytics architecture.

```text
Source Data
    |
    v
RAW
    |
    v
STAGING
    |
    v
INTERMEDIATE
    |
    v
MARTS
    |
    v
ANALYTICS
    |
    v
Tableau Dashboards
```

Apache Airflow orchestrates the dbt workflow, which transforms data and runs quality tests in Snowflake.

```text
Apache Airflow
      |
      v
   dbt build
      |
      +--> Transform data
      |
      +--> Run data quality tests
      |
      v
Snowflake Analytics Models
      |
      v
Tableau
```

## Dataset Overview

The project uses generated sample data representing a fictional data quality SaaS platform.

| Entity | Records |
|---|---:|
| Customers | 20 |
| Data sources | 50 |
| Pipelines | 75 |
| Pipeline runs | 21,225 |
| Data assets | 150 |
| Quality checks | 450 |
| Quality check results | 13,500 |

### Pipeline Run Results

| Status | Runs |
|---|---:|
| Successful | 20,292 |
| Failed | 933 |
| Total | 21,225 |

The overall pipeline success rate in the generated dataset is approximately **95.60%**.

## dbt Data Modeling

The dbt project transforms raw data into analytical models through staging, intermediate, and reporting layers.

Key analytical models:

- `mart_customer_quality` — customer-level quality metrics.
- `mart_asset_quality` — asset-level quality monitoring.
- `mart_quality_dimension` — quality metrics by dimension.
- `mart_pipeline_reliability` — pipeline execution and reliability metrics.

These models support analysis of failed quality results, pass rates, asset criticality, pipeline failures, and execution duration.

### dbt Build and Testing

The recorded successful dbt build included:

- 13 models.
- 68 tests.
- 82 successful model and test execution results combined.
- No warnings or errors.

The project uses explicit, interpretable metrics rather than an opaque composite quality score.

## Apache Airflow Orchestration

The Airflow DAG is named `data_quality_saas`.

- **Schedule:** Daily at 06:00.
- **Task:** `run_dbt_build`.
- **Purpose:** Execute the dbt build workflow.

A manual DAG run completed successfully, with 13 models passing and no warnings or errors in the recorded run.

The local Airflow environment runs using Docker Compose.

## Tableau Dashboards

Four dashboards were developed to monitor data quality and pipeline reliability.

### 1. DataTrust | Customer Quality Overview

Provides a customer-level overview of quality performance.

- Total Failed Results
- Overall Quality Pass Rate
- Failed Quality Results by Customer
- Customer Pass Rate

### 2. DataTrust | Asset Quality Monitoring

Monitors data asset quality and potential problem areas.

- Failed Results by Assets
- Asset Pass Rate
- Asset Criticality
- Failed Dimensions by Assets

### 3. DataTrust | Quality Dimensions

Compares quality performance across quality dimensions.

- Failed Results by Dimension
- Pass Rate by Dimension
- Total Results by Dimension

### 4. DataTrust | Pipeline Reliability

Monitors execution outcomes and pipeline performance.

- Pipeline Run Status
- Pipeline Success Rate
- Pipeline Run Duration
- Failed Runs by Pipeline

**Tableau Public:** Add the published workbook URL here once all four dashboards are accessible from the public workbook.

## Key Metrics

The project uses straightforward operational metrics that are easy for business and technical stakeholders to interpret.

- **Quality pass rate:** Percentage of quality check results that pass.
- **Failed quality results:** Count of failed quality check results.
- **Pipeline success rate:** Percentage of pipeline runs that succeed.
- **Pipeline run duration:** Average and maximum execution duration.
- **Asset quality:** Quality results analyzed by data asset and criticality.
- **Dimension quality:** Pass and failure results grouped by quality dimension.

Rates are stored on a 0–100 scale in the exported dashboard data.

## Running the Project

The project uses a local development environment connected to Snowflake.

Typical workflow:

1. Configure Snowflake credentials and the dbt profile.
2. Verify the Snowflake connection.
3. Run dbt models and tests.
4. Review the analytical models in Snowflake.
5. Run the Airflow DAG to orchestrate the dbt build.
6. Export analytical data for Tableau when needed.
7. Review dashboards and investigate quality or reliability issues.

Example dbt commands:

```bash
dbt debug
dbt build
```

Run these commands from the configured dbt project directory and environment.

## Project Scope and Future Enhancements

- The data represents a fictional SaaS platform, not a real customer's production environment.
- Tableau dashboard data is exported from Snowflake as CSV files.
- Airflow orchestration has been tested locally.
- Automated alert notifications, SLA enforcement, and integrated dashboard refreshes are potential future enhancements.

## Skills Demonstrated

- Analytics engineering
- SQL and data modeling
- Snowflake data warehousing
- dbt transformations and testing
- Apache Airflow orchestration
- Data quality monitoring
- Pipeline reliability analytics
- Tableau dashboard development
- Git and GitHub workflows

---

**Project:** DataTrust Data Quality & Observability SaaS  
**Purpose:** Analytics engineering portfolio project
