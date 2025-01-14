from langgraph.checkpoint.memory import MemorySaver

# TODO: 本来はメモリをDB化する。プロジェクトやスレッドのIDをキーにする？
memory = MemorySaver()