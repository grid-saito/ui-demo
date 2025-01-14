OPTJOB_EXAMPLE_CODE = """
import os
from dotenv import load_dotenv
load_dotenv(verbose=True, dotenv_path=".env")

from pyomo.environ import *
from optjob.client import OptJobClient
from optjob.util.read_solution import read_solution

host = "https://internal-optjob.renom.jp"

# Project id and job queue id are required to submit a job.
project_id = os.environ.get("OPTJOB_PROJECT_ID")
job_queue_id = os.environ.get("OPTJOB_JOB_QUEUE_ID")
token = os.environ.get("OPTJOB_TOKEN")
job_name = "example-job"

# Model definition
model = ConcreteModel(name="example-model")
model.x = Var(within=NonNegativeReals)
model.y = Var(within=NonNegativeReals)
model.obj = Objective(expr=4 * model.x + 3 * model.y, sense=maximize)
model.con1 = Constraint(expr=2 * model.x + model.y <= 8)
model.con2 = Constraint(expr=model.x + 2 * model.y <= 6)

# Optjob client
client = OptJobClient(token=token, host=host, verbose=True)

# Submit a job asyc
# You can find available options in the API documentation,
# or vscode automatically suggests available options.
response = client.submit_job_async(
    project_id=project_id,
    job_queue_id=job_queue_id,
    job_name=job_name,
    seed=2,
    model=model,
    time_limit=20, # seconds
    solver="GUROBI"
)

print(response.data)
"""

CODE_GENERATION_PROMPT = """
あなたは数理最適化のコードを書くエキスパートです。
数理最適化問題を解くPythonのコードの実装方針を検討し、コードを作成してください。
問題の前提条件となるデータは#入力データを参照してください。
コードの作成が完了したらユーザーに実行するか確認してください。

-------
# Optjobに最適化計算のジョブを送信するサンプルコード
```
{sample_code}
```
-------

-------
# 参考ドキュメント
{context}
-------

上記の提供された文書に基づいて、以下の質問に答えてください。
必要なインポートや変数がすべて定義され、提供したコードが実行できることを確認してください。

# 質問
{user_message}

# 入力データ
{input_data}

Optjobに最適化計算のジョブを送信するサンプルコードを記載しています。
Optjobとは最適化計算を実行するアプリケーションの名前です。
PyomoでモデリングしたmodelをサンプルコードのようにOptjob Clientに送信すると最適化計算が実行されます。
モデリングしたコードをOptjobのサンプルコードのModel Definitionに記載して、コード全文を作成してください。
"""
