from typing import TypedDict, Annotated, Sequence, Literal
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
import operator
from langchain_core.messages import BaseMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.graph import END, START, StateGraph, MessagesState
from langgraph.prebuilt import ToolNode

# Load environment variables from .env file
load_dotenv()

# Define a custom state class that includes fields for agents' messages
class MultiAgentState(TypedDict):
    draft_messages: Annotated[Sequence[BaseMessage], operator.add]
    reviewer_messages: Annotated[Sequence[BaseMessage], operator.add]
    next: str

# ---- Step 1: Define the Sanity.io Stub Functions ----
def get_latest_prompts_from_sanity():
    """Retrieve latest prompts from Sanity.io (Stub Function)."""
    # Simulate getting prompts from Sanity (returns a hard-coded string)
    print ('Get a prompt from sanity.io')
    return "Focus on tech burnout themes and use action-oriented language."

def count_words(text):
    words = text.split()
    return len(words)

def insert_draft_into_sanity(content, platform):
    """Stub function to insert drafts into Sanity.io."""
    print(f"Inserting draft for {platform}: {count_words(content)} words")

    # Simulate a successful insertion
    return {"status": "success", "id": "draft123"}

# ---- Step 2: Define the State for LangGraph ----
class State(TypedDict):
    messages: Annotated[list, add_messages]

# ---- Step 3 define agent functions ---
# tools
@tool


def save_content(t: str):
    """
        Insert text content into Sanity.io for review and platform distribution.
        This function uploads the content to Sanity for both Substack and X platforms.
    """
    print(f"Saving content: {t}")
    insert_draft_into_sanity(t, platform='Substack')
    insert_draft_into_sanity(t, platform='X')


def x_post():
    """
        Calls the X platform API to publish a post. Stub function.
    """
    print("Posting to the X platform API")

tools = [save_content, x_post]
tool_node = ToolNode(tools)

# LLM agent
llm = ChatOpenAI(model="gpt-4o").bind_tools(tools)

def draft(state: State):
    print ('running draft model agent')
    return {"messages": [llm.invoke(state["messages"])]}

# ---- Step 4: Integrate Agent Functions into the LangGraph Framework ----

# Init StateGraph for 2 nodes, draft agent and tools to output the generated content
# Establish connections between nodes in the graph
workflow = StateGraph(State)
workflow.add_node("agent", draft)
workflow.add_node("tools", tool_node)
workflow.add_edge(START, "agent")
workflow.add_edge("tools", "agent")

# Function that determines  to continue or not
def should_continue(state: MessagesState) -> Literal["tools", END]:
    messages = state['messages']
    last_message = messages[-1]
    print('should continue')
    # If the LLM makes a tool call, then we route to the "tools" node
    if last_message.tool_calls:
        return "tools"
    # Otherwise, we stop (reply to the user)
    return END

# We now add a conditional edge
workflow.add_conditional_edges(
    # First, we define the start node. We use `agent`.
    # This means these are the edges taken after the `agent` node is called.
    "agent",
    # Next, we pass in the function that will determine which node is called next.
    should_continue,
)

# Initialize memory to persist state between graph runs
checkpointer = MemorySaver()

# Compile the graph
app = workflow.compile(checkpointer=checkpointer)
print('Starting the book launch app - v 0.1')
final_state = app.invoke(
    {"messages": [SystemMessage(content=get_latest_prompts_from_sanity())]},
    config={"configurable": {"thread_id": 42}}
)

#print(final_state["messages"][-1].content)