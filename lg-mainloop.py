import operator
from typing import TypedDict, Annotated, Sequence
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from bl_sanity_utils import get_system_prompt, insert_post, get_cycle, set_cycle

# Rev 2 Simplified routing
# Load environment variables from .env file
load_dotenv()

# Define a custom state class that includes fields for agents' messages
class MultiAgentState(TypedDict):
    draft_messages: Annotated[Sequence[BaseMessage], operator.add]
    reviewer_messages: Annotated[Sequence[BaseMessage], operator.add]
    next: str

# ---- Step 1: Define tool Functions ----

def count_words(text):
    words = text.split()
    return len(words)

def insert_draft_into_sanity(content):
    """
        insert drafts into Sanity.io.
        :param content:
    """
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

# ---- Step 3 define node functions that run on the graph ---
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
    print ('\nRunning the Draft model agent')
    return {"messages": [llm.invoke(state["messages"])]}


def literary_critic(state: State):
    print('\nRunning the Literary critic model agent')
    # Content from the previous state
    response = state["messages"]
    draft_content = response[1].content
    critic_system_prompt = get_system_prompt(0)
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
print('Starting the book launch app - v 0.50')

current_cycle = get_cycle()
print('This round is:', current_cycle)
system_prompt = get_system_prompt(current_cycle)
print('System Prompt\n\n')
print(system_prompt)
print('\n-------------------------------------------------------------\n')
set_cycle()
next_cycle = get_cycle()
print('Next round will be:', next_cycle)
print('\n-------------------------------------------------------------\n')
final_state = app.invoke(
    {"messages": [SystemMessage(content=system_prompt)]},
    config={"configurable": {"thread_id": 42}}
)

#print(final_state["messages"][-1].content)