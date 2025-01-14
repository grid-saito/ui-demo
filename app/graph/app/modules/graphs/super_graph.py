from langgraph.graph import END, START, StateGraph
from modules.data_models.graph_state import GraphState
#from modules.edges.code_confirm_router import code_execution_router
#from modules.edges.code_router import code_router
from modules.edges.initial_router import initial_router
from modules.edges.input_confirm_router import input_confirm_router
#from modules.edges.input_router import input_router
#from modules.edges.result_router import result_router
#from modules.nodes.code_team import (code_execution, code_generation,
#                                     code_review, code_supervisor,
#                                     code_visualization)
from modules.nodes.initialize import initialize
from modules.nodes.input_team.input_confirmation import input_confirmation
from modules.nodes.input_team.input_data_processing import input_data_processing 
#from modules.nodes.result_team import (result_polling, result_supervisor,
#                                       result_visualization)
from modules.memories.super_graph_memory import memory


def create_super_graph():
    """
    Creates and compiles the super graph with the specified nodes and edges.
    """
    # Initialize the graph builder
    graph_builder = StateGraph(GraphState)

    # Add nodes
    graph_builder.add_node("initialize", initialize)
    graph_builder.add_node("input_data_processing_node", input_data_processing)
    graph_builder.add_node("input_confirmation_node", input_confirmation)
    
    # Add edges
    graph_builder.add_edge(START, "initialize")  # Start to initialize
    graph_builder.add_edge("initialize", "input_data_processing_node")  # Start to initialize
    graph_builder.add_edge("input_data_processing_node", "input_confirmation_node") 
    graph_builder.add_edge("input_confirmation_node", END) 
    #graph_builder.add_conditional_edges("input_confirmation_node", input_confirm_router)
    
    # Compile the graph
    super_graph = graph_builder.compile(
        interrupt_before=["input_confirmation_node"],  # Interrupt before data processing
        checkpointer=memory,  # Use the defined memory for checkpointing
    )
    return super_graph


