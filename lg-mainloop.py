import operator
from typing import TypedDict, Annotated, Sequence
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from bl_sanity_utils import insert_sanity_document

# Rev 2 Simplified routing
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
    p = "What is a great strategy for women over 45 with small children and burnout in tech? Make the response especially attractive for women with good jobs working in biotechnology in the Bay area. Return the prompt in the first line of the post as the title"

    print (f"Prompt is {p}")
    return p

def count_words(text):
    words = text.split()
    return len(words)

def insert_draft_into_sanity(content):
    """Stub function to insert drafts into Sanity.io."""
    title = content.split('\n')[0].replace('*','').replace('#','')
    newline_index = content.find('\n')
    if newline_index != -1:
        body = content[newline_index + 1:]
    else:
        body = content
    print(f"Body: {body}")
    print('--------------------------------------------')
    print(f"Inserting draft: {count_words(content)} words \n Title: {title} \n Body: {body}")
    insert_sanity_document(title, body)
    # put return code handling here
    return {"status": "success", "id": "draft123"}



# ---- Step 2 define LLM
llm = ChatOpenAI(model="gpt-4o-mini")

# ---- Step 3: Define the State for LangGraph ----
class State(TypedDict):
    messages: Annotated[list, add_messages]

# --- Step 4: Define nodes ---
def draft_writer(state: State):
    print ('running draft model agent')
    return {"messages": [llm.invoke(state["messages"])]}

def save_content(state: State):
    """
        Insert text content into Sanity.io for review and platform distribution.
        This function uploads the content to Sanity for both Substack and X platforms.
    """
    response = state["messages"]
    # response contains a list of objects
    # SystemMessage := response[0].content
    # AIMessage := response[1].content
    t= response[1].content
    insert_draft_into_sanity(t)

# ---- Step 4: Integrate Agent Functions into the LangGraph Framework ----

# Init StateGraph for 2 nodes
# Establish connections between nodes in the graph
# draft -> save -> END
workflow = StateGraph(State)
workflow.add_node("draft", draft_writer)
workflow.add_node("save", save_content)
workflow.add_edge(START, "draft")
workflow.add_edge("draft", "save")
workflow.add_edge("save", END)

# Initialize memory to persist state between graph runs
checkpointer = MemorySaver()

# Compile the graph
app = workflow.compile(checkpointer=checkpointer)
print('Starting the book launch app - v 0.3')
final_state = app.invoke(
    {"messages": [SystemMessage(content=get_latest_prompts_from_sanity())]},
    config={"configurable": {"thread_id": 42}}
)

#print(final_state["messages"][-1].content)