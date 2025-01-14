# LangGraphを使ってサンプル生成
import logging

from langchain_core.messages import HumanMessage
from modules.graphs.super_graph import create_super_graph
from modules.data_models.graph_state import GraphState
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    super_graph = create_super_graph(GraphState)
    graph_config = {
        "configurable": {"thread_id": 1},
    }
    input_text = input("input: ")
    result = super_graph.invoke(
        {"messages": [HumanMessage(content=input_text)]}, config=graph_config
    )
    print(type(result))
    print(result)
    print(f"last_message: {result['messages'][-1].content}")
    print(f"next: {result['next']}")

    while True:
        input_text = input("input: ")
        if input_text == "":
            continue
        if input_text == "q":
            break

        super_graph.update_state(
            graph_config, {"messages": [HumanMessage(content=input_text)]}
        )
        result = super_graph.invoke(None, config=graph_config)
        print(result)
        print(f"last_message: {result['messages'][-1].content}")
        print(f"next: {result['next']}")


if __name__ == "__main__":
    main()
