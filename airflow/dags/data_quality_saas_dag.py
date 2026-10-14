
from datetime import datetime

from airflow.sdk import dag, task
import subprocess


@dag(
    dag_id="data_quality_saas",
    start_date=datetime(2026, 1, 1),
    schedule="0 6 * * *",
    catchup=False,
    tags=["dbt", "data-quality"],
)
def data_quality_saas():

    @task
    def run_dbt_build():

        try:
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
            if result.stderr:
                print(result.stderr)

        except subprocess.CalledProcessError as exc:
            print(f"dbt build failed with exit code: {exc.returncode}")

            if exc.stdout:
                print("dbt stdout:")
                print(exc.stdout)

            if exc.stderr:
                print("dbt stderr:")
                print(exc.stderr)

            raise

        print(result.stdout)
        print(result.stderr)

    run_dbt_build()


data_quality_saas()