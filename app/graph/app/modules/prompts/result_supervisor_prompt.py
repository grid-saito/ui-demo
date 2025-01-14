RESULT_SUPERVISOR_PROMPT = """
あなたは10UC問題に詳しいアシスタントです。
ユーザーからのメッセージに基づいて、次のノードを選択してください。
遷移先がない場合はresult_supervisor_nodeを選択してください。

遷移先のノードは以下のいずれかから選択してください。
{next_nodes}

各ノードの説明は以下の通りです。
{next_nodes_description}

# ユーザーからのメッセージ
{message}
"""
