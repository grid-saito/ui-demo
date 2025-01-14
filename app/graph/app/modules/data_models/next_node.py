from pydantic import BaseModel, Field


class NextNode(BaseModel):
    node_name: str = Field(description="次のノードの名前")


class InputNextNode(BaseModel):
    node_name: str = Field(description="次のノードの名前")
    input_data_confirmation: bool = Field(description="入力データを承認するかどうか")


class CodeNextNode(BaseModel):
    node_name: str = Field(description="次のノードの名前")
    code_confirmation: bool = Field(description="コードを承認し、実行するかどうか")


class ResultNextNode(BaseModel):
    node_name: str = Field(description="次のノードの名前")
