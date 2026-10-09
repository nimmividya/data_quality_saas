
from datetime import datetime

from airflow.sdk import dag, task
import subprocess


@dag(
    dag_id="data_quality_saas",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["dbt", "data-quality"],
)
def data_quality_saas():

    @task
    def run_dbt_build():
        result = subprocess.run(
            [
                "dbt",
                "build",
                "--project-dir",
                "/opt/airflow/data_quality_saas",
                "--profiles-dir",
                "/opt/airflow/.dbt",
            ],
            check=True,
            capture_output=True,
            text=True,
        )

        print(result.stdout)
        print(result.stderr)

    run_dbt_build()


data_quality_saas()