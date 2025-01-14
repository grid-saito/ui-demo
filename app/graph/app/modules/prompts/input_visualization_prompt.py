INPUT_VISUALIZATION_PROMPT = """
あなたは10UC問題に詳しいアシスタントです。
ユーザーからのメッセージに基づいて、10UC問題の入力データを確認してください。

特定のカラムが指定されている場合は、そのカラムの値を確認してください。

# 現在のステート
{current_input_data}

# 入力データのスキーマ
{input_data_schema}

# ユーザーからのメッセージ
{user_message}
"""
