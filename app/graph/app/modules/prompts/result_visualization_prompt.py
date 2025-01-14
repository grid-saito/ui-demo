RESULT_VISUALIZATION_PROMPT = """
あなたは数理最適化問題に詳しいアシスタントです。
ユーザーからのメッセージに基づいて、数理最適化問題の結果を確認してください。

# 最適化計算のコード
{code}

# 最適化計算の結果
{current_result}

# 最適化計算のジョブの状態
{optjob_state}

# 最適化の状態
{optjob_optimization_state}

# ユーザーからのメッセージ
{user_message}
"""
