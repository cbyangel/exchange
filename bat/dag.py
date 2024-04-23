import os
import pendulum as p
from textwrap import dedent
from airflow import DAG
from airflow.operators.bash import BashOperator
# from airflow.providers.slack.notifications.slack import send_slack_notification

script_dir = os.path.dirname(__file__)


description = 'usd_krw_prediction'
start_date = p.datetime(2024,4,22,0,0,0, tz='Asia/Seoul')
schedule_interval='0 9,12,15 * * *' # minute hour day month dow : based on KST

dag = DAG(
    dag_id = 'usd_krw_prediction_v1',
    start_date = start_date,
    schedule_interval = schedule_interval,
    concurrency = 1,
    catchup = False
)

t1 = BashOperator(
    task_id='prepare_data',
    bash_command=f'{script_dir}/prepare_data.sh ',
    dag=dag
)
    
t2 = BashOperator(
    task_id='make_features',
    bash_command=f'{script_dir}/make_features.sh ',
    dag=dag
)

t3 = BashOperator(
    task_id='predict',
    bash_command=f'{script_dir}/predict.sh ',
    dag=dag
)

t1 >> t2 >> t3

# if __name__ == "__main__":
#     dag.cli()