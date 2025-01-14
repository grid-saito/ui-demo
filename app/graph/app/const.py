input_node_description = {
    "input_supervisor_node": "データ入力に関するユーザーのメッセージを受け付けるノード。次のノードを選択する機能を持つ。",
    "input_data_node": "ユーザーから問題の前提条件となる入力データを受け取った場合は、input_data_nodeに遷移してグラフのステートを更新する。データが足りているかどうかの確認も行う。",
    "input_visualization_node": "ユーザーから問題の前提条件について質問を受けた場合に、input_visualization_nodeに遷移してグラフのステートに保存している入力データを表示する。",
    "input_confirmation_node": "ユーザーがコード生成の状態に遷移することを指示した場合に、input_confirmation_nodeに遷移する。",
}

code_node_description = {
    "code_supervisor_node": "最適化問題のモデリングに関するユーザーのメッセージを受け付けるノード。次のノードを選択する機能を持つ。",
    "code_generation_node": "ユーザーからコードの可視化に関する指示を受けた場合に、code_generation_nodeに遷移してコードを生成する。または、現在のコードを編集する。",
    "code_visualization_node": "ユーザーからコードの可視化に関する指示を受けた場合に、code_visualization_nodeに遷移してグラフのステートに保存しているコードを表示する。",
    "code_execution_node": "ユーザーからコードの実行に関する指示を受けた場合に、code_execution_nodeに遷移してグラフのステートに保存しているコードを実行する。",
}

result_node_description = {
    "result_supervisor_node": "最適化問題の結果に関するユーザーのメッセージを受け付けるノード。次のノードを選択する機能を持つ。",
    "result_visualization_node": "ユーザーから最適化問題の結果の可視化に関する指示を受けた場合に、result_visualization_nodeに遷移してグラフのステートに保存している結果を表示する。",
}

initialize_next_nodes = ["input_processing_node"]

input_supervisor_next_nodes = [
    "input_supervisor_node",
    "input_data_node",
    "input_visualization_node",
    "input_confirmation_node",
]

code_supervisor_next_nodes = [
    "code_supervisor_node",
    "code_generation_node",
    "code_visualization_node",
    "code_execution_node",
]

result_supervisor_next_nodes = [
    "result_supervisor_node",
    "result_visualization_node",
]
