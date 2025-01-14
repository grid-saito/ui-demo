from pydantic import BaseModel, Field

class SuggestedActionsOutput(BaseModel):
    actions: list[str] = Field(description="推奨されるアクションのリスト")
