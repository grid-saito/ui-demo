from pydantic import BaseModel, Field

INPUT_DATA_SCHEMA = """
class InputData(BaseModel):
    num_units: int = Field(description="ユニット数")
    max_output: list[int] = Field(description="各ユニットの最大出力")
    startup_cost: list[int] = Field(description="各ユニットの起動コスト")
    operating_cost: list[int] = Field(description="各ユニットの稼働コスト")
    shutdown_cost: list[int] = Field(description="各ユニットの停止コスト")
    demand: list[int] = Field(description="各タイムステップの需要")
"""


class InputData(BaseModel):
    num_units: int = Field(default=0, description="ユニット数")  # Default to 0 units
    max_output: list[int] = Field(default_factory=list, description="各ユニットの最大出力")
    startup_cost: list[int] = Field(default_factory=list, description="各ユニットの起動コスト")
    operating_cost: list[int] = Field(default_factory=list, description="各ユニットの稼働コスト")
    shutdown_cost: list[int] = Field(default_factory=list, description="各ユニットの停止コスト")
    demand: list[int] = Field(default_factory=list, description="各タイムステップの需要")

    @property
    def data_schema(self):
        return INPUT_DATA_SCHEMA


class InputDataNodeOutput(BaseModel):
    input_data: InputData = Field(
        default_factory=InputData, description="10UC問題の入力データ"
    )
    missing_data: list[str] = Field(
        default_factory=list, description="入力データに不足しているデータ"
    )
    response_message: str = Field(
        default="", description="ユーザーに返答するメッセージ"
    )
    input_data_confirmation: bool = Field(
        default=False, description="ユーザーの入力データの承認状態"
    )


class InputDataGraphState(BaseModel):
    input_data: InputData = Field(
        default_factory=InputData, description="10UC問題の入力データ"
    )
    input_data_confirmation: bool = Field(
        default=False, description="ユーザーの入力データの承認状態"
    )