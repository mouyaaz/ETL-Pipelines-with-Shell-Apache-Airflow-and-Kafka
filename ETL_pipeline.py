from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime

def python_transform():
    import pandas as pd
    df = pd.read_csv('data.csv')
    df['city'] = df['city'].str.upper()
    df.to_csv('data_transformed_python.csv', index=False)
    print("Data transformed using Python")

default_args = {
    'owner': 'mustapha',
    'start_date': datetime(2024, 8, 1),
}

with DAG('etl_pipeline',
         default_args=default_args,
         schedule_interval='@daily',
         catchup=False) as dag:

    extract = BashOperator(
        task_id='extract',
        bash_command='./extract.sh'
    )

    transform_bash = BashOperator(
        task_id='transform_bash',
        bash_command='./transform.sh'
    )

    transform_python = PythonOperator(
        task_id='transform_python',
        python_callable=python_transform
    )

    load = BashOperator(
        task_id='load',
        bash_command='./load.sh'
    )

    # Using bash transform
    extract >> transform_bash >> load

    # Alternatively, using python transform
    # extract >> transform_python >> load
