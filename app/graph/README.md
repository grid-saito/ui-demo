# プロジェクト

対話的に最適化計算を実施し、結果を確認するプロジェクト

# Requirements

- Optjob Python client

https://gitlab.com/grid-devs/apps/optjob/python-client


# ディレクトリ構造

```
.
├── app
│   ├── modules
│   │   ├── chains
│   │   ├── data_models
│   │   ├── edges
│   │   ├── graphs
│   │   ├── memories
│   │   ├── models
│   │   ├── nodes
│   │   ├── optjob
│   │   ├── prompts
│   │   ├── retreivers
│   │   ├── slack_apps
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── sample.py
├── requirements.txt
└── README.md
```

# モジュールのサンプル

### prompts

プロンプトのテンプレートを記載する。

```
XXX_PROMPT = """
プロンプト

# ユーザーからのメッセージ
{message}  # 変数はテンプレートの形式で定義する
"""
```

### data_models

Pydanticのデータモデルを定義する。  
データモデルはStructuredOutputやGraphのStateとして使用する。

```
class GraphState(BaseModel):
    messages: Annotated[List[BaseMessage], operator.add] = Field(
        description="チャット履歴"
    )
    response_message: str = Field(
        description="ユーザーに返答するメッセージ", default=""
    )
    next: str = Field(description="次のノード", default="")
    ...
```

### models

モデルを定義する。  
Azure以外を使う場合は適宜ファイルを作成して追加する。

```
langchain_azure_model = AzureChatOpenAI(
    azure_deployment=AZURE_OPENAI_DEPLOYMENT_NAME,
    model=AZURE_OPENAI_MODEL,
    api_key=AZURE_OPENAI_API_KEY,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
)

langchain_azure_embeddings_model = AzureOpenAIEmbeddings(
    azure_deployment=AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT_NAME,
    model=AZURE_OPENAI_EMBEDDINGS_MODEL,
)

```

### chains

チェーンを定義する。  
基本形は以下の通り。（本来はベースクラスを作りたいが一旦この形式で）

```
structured_model = langchain_azure_model.with_structured_output(XXX_DATA_MODEL)
chain = (
    ChatPromptTemplate.from_template(XXX_PROMPT) |
    structured_model
)
```

### edges

ConditionalEdgeを定義する。  
Node側でLLMを使って次のNodeを判断するグラフになっているので、Edge側にはほとんど処理を記述しない。

```
def initial_router(state: GraphState):
    logger.info("Call initial_router...")
    logger.info(f"Next node: {state.next}")
    return state.next
```

### nodes

ノードを定義する。  
LLMの処理を行う場合はチェーンをimportして使用する。

ノードの定義はstateを引数に持つ関数の形式で行い、stateを更新して返す。  
returnしたstateがグラフ全体のStateになる。

```
def some_node(state: GraphState):
    ...
    return state
```

### memories

メモリを定義する。  
本来はDBをメモリとして使用する。


### optjob

Optjobのクライアント定義とクライアントを使用する関数を定義する。
