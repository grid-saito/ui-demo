from pydantic import BaseModel, Field


class Code(BaseModel):
    code: str = Field(description="実行可能なpythonのコード", default="")


class CodeGraphState(BaseModel):
    background: str = Field(description="背景", default="")
    parameter: str = Field(description="パラメータ", default="")
    constraint: str = Field(description="制約", default="")
    variables: str = Field(description="変数", default="")
    objective: str = Field(description="目的関数", default="")
    solution_status: str = Field(description="解の状態", default="")
    error_message: str = Field(description="エラーメッセージ", default="")
    rounds: int = Field(description="反復回数", default=0)
    program: str = Field(description="プログラム", default="")


class CodeNodeOutput(BaseModel):
    code: Code = Field(description="実行可能なpythonのコード", default=Code())
    response_message: str = Field(
        description="ユーザーに返答するメッセージ", default=""
    )
