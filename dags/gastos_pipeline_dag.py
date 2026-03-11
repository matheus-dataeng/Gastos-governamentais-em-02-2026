import pendulum
import logging as log
from airflow import DAG
from airflow.operators.python import PythonOperator
from bronze.extract import extract
from silver.transform import transform
from gold.build_metrics import build_metrics
from gold.load import load

with DAG(
    dag_id="gastos_governamentais",
    description="Gasto do governo em fevereiro de 2026",
    start_date=pendulum.datetime(2026, 1, 15, tz="America/Sao_Paulo"),
    schedule=None,
    catchup=False,
    tags=["Projeto", "Gastos do Governo"]
) as dag:

    extract_task = PythonOperator(
        task_id="extract",
        python_callable=extract
    )
    
    transform_task = PythonOperator(
        task_id="transform",
        python_callable=transform
    )
    
    build_metrics_task = PythonOperator(
        task_id="build_metrics",
        python_callable=build_metrics
    )
    
    load_task = PythonOperator(
        task_id="load",
        python_callable=load
    )
      
    extract_task >> transform_task >> build_metrics_task >> load_task