import logging

from langchain_core.messages import HumanMessage
from config import SLACK_BOT_TOKEN
from slack_bolt import App

from modules.graphs.super_graph import super_graph

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = App(token=SLACK_BOT_TOKEN)

running_thread_ids = []

def extract_thread_ts(event) -> str:
    return event.get("thread_ts", None) or event["ts"]


def extract_file_info(event) -> list[dict]:
    return event.get("files", [])


def extract_message(event) -> str:
    return event.get("text", "")


def no_bot_messages(message, next):
    subtype = message.get("subtype")
    if subtype != "bot_message":
        next()


def pipeline(event, say, context):
    logger.info("call pipeline...\n\n")
    logger.info(f"event: {event}\n\ncontext: {context}\n\n")

    thread_ts = extract_thread_ts(event)
    message = extract_message(event)
    graph_config = {
        "configurable": {"thread_id": thread_ts},
    }
    logger.info(f"thread_ts: {thread_ts}\n\nmessage: {message}\n\n")

    if thread_ts not in running_thread_ids:
        logger.info(f"Thread is not exists in running_thread_ids. Invoke super_graph with human message.\n\n")
        running_thread_ids.append(thread_ts)
        result = super_graph.invoke(
            {"messages": [HumanMessage(content=message)]},
            config=graph_config
        )
    else:
        logger.info(f"Thread is exists in running_thread_ids. Continue super_graph invoking.\n\n")
        super_graph.update_state(
            graph_config,
            {"messages": [HumanMessage(content=message)]}
        )
        result = super_graph.invoke(
            None,
            config=graph_config
        )

    logger.info(f"Result: {result}\n\n")
    result_message = result["messages"][-1].content
    say(result_message, thread_ts=thread_ts)


@app.event("message", middleware=[no_bot_messages])
def respond_to_dm(event, say, context):
    logger.info("call respond_to_dm...\n\n")
    pipeline(event, say, context)


@app.event("app_mention", middleware=[])
def respond_to_mention(event, say, context):
    logger.info("call respond_to_mention...\n\n")
    pipeline(event, say, context)
