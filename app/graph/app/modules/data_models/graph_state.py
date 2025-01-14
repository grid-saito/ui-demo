import operator
from typing import Annotated, Any, List

from langchain_core.messages import BaseMessage
from modules.data_models.code import Code
from modules.data_models.input_data import InputData
from pydantic import BaseModel, Field
from modules.data_models.external_source import WeatherData, DemandData, PlantStatus


class GraphState(BaseModel):
    messages: Annotated[List[BaseMessage], operator.add] = Field(
        description="チャット履歴"
    )
    # dev: whats the difference between messages and response_message?
    response_message: str = Field(
        description="ユーザーに返答するメッセージ", default=""
    )
    next: str = Field(description="次のノード", default="")
    # 人間のチェックポイントを仮置き
    input_data_confirmation: bool = Field(description="入力データの確認", default=False)
    code_confirmation: bool = Field(description="コードの確認", default=False)
    code_success: bool = Field(description="コードの実行", default=False)
    result_confirmation: bool = Field(description="結果の確認", default=False)
    # OptjobのジョブID
    optjob_job_id: str = Field(description="OptjobのジョブID", default="")
    optjob_job_name: str = Field(description="Optjobのジョブ名", default="")
    optjob_model: Any = Field(
        description="Optjobのモデル", default=None
    )
    optjob_result: str | None = Field(description="Optjobの結果", default=None)
    optjob_score: float | None = Field(description="Optjobのスコア", default=None)
    optjob_state: str | None = Field(description="Optjobの状態", default=None)
    optjob_optimization_state: str | None = Field(
        description="Optjobの最適化状態", default=None
    )
    
    # サブグラフのState
    input_data: InputData | None = Field(description="入力データ")
    code: Code | None = Field(description="コード", default=None)
    weather_data: WeatherData | None = Field(description="現在の各拠点の気象")
    demand_data: DemandData | None = Field(description="各地域の電力需要")
    plant_status: PlantStatus | None = Field(description="拠点ごとのプラントのステート")