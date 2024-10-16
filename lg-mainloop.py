import operator
from typing import TypedDict, Annotated, Sequence
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from bl_sanity_utils import get_system_prompt, insert_post

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
    """Retrieve today's prompt from Sanity.io (Stub Function)."""
    return get_system_prompt()


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
    #print(f"Body: {body}")
    #print('--------------------------------------------')
    #print(f"Inserting draft: {count_words(content)} words \n Title: {title} \n Body: {body}")
    insert_post(title, body)
    return {"status": "success", "id": "draft123"}


# ---- Step 2 define LLM
llm = ChatOpenAI(model="gpt-4o-mini")

# ---- Step 3: Define the State for LangGraph ----
class State(TypedDict):
    messages: Annotated[list, add_messages]

# ---- Step 3 define functions that run on the graph ---
def save_content(state: State):
    """
        Insert text content into Sanity.io for review and platform distribution.
        This function uploads the content to Sanity for both Substack and X platforms.
    """
    print ('\nRunning the Save content agent')
    response = state["messages"]
    # response contains a list of objects
    # SystemMessage := response[0].content
    # AIMessage := response[1].content
    t = response[1].content
    insert_draft_into_sanity(t)

def draft_writer(state: State):
    print ('\nRunning the draft model agent')
    return {"messages": [llm.invoke(state["messages"])]}


def literary_critic(state: State):
    print('\nRunning the literary critic model agent')
    # Content from the previous state
    response = state["messages"]
    draft_content = response[1].content
    critic_system_prompt = (
        "This is a draft of a post for X for my latest book - Bob and Alice - an anti-love story"
        "Edit it so that it will score a perfect score of 10 for people who work in tech in California"
        "Use language that jives with people age 25-39"
        "Add emojis in the header to make it more appealing and shareable on social media"
        "Keep the romance flowing"
    )
    state["messages"] = [
        {"role": "system", "content": critic_system_prompt},
        {"role": "user", "content": draft_content},
    ]

    response = llm.invoke(state["messages"])
    ai_message_content = response.content

    # Append the AI-generated message to the state messages
    state["messages"].append({"role": "assistant", "content": ai_message_content})

    # Return the updated state
    return state


# ---- Step 5: Integrate Agent Functions into the LangGraph Framework ----
# Define the workflow logic
workflow = StateGraph(State)

# Nodes
workflow.add_node("draft", draft_writer)
workflow.add_node("critic", literary_critic)
workflow.add_node("save", save_content)

# Edges
workflow.add_edge(START, "draft")
workflow.add_edge("draft", "critic")
workflow.add_edge("critic", "save")
workflow.add_edge("save", END)

# Initialize memory to persist state between graph runs
checkpointer = MemorySaver()

# Compile the graph
app = workflow.compile(checkpointer=checkpointer)
print('Starting the book launch app - v 0.47')
print('System Prompt\n\n')
print(get_latest_prompts_from_sanity())
print('\n-------------------------------------------------------------\n')

final_state = app.invoke(
    {"messages": [SystemMessage(content=get_latest_prompts_from_sanity())]},
    config={"configurable": {"thread_id": 42}}
)

#print(final_state["messages"][-1].content)