from typing import Annotated
from langchain_openai import ChatOpenAI
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ---- Step 1: Define the Sanity.io Stub Functions ----
def get_latest_prompts_from_sanity():
    """Retrieve latest prompts from Sanity.io (Stub Function)."""
    # Simulate getting prompts from Sanity (returns a hard-coded string)
    return "Focus on tech burnout themes and use action-oriented language."

def insert_draft_into_sanity(content, platform):
    """Stub function to insert drafts into Sanity.io."""
    print(f"Inserting draft for {platform}: {content}")
    # Simulate a successful insertion
    return {"status": "success", "id": "draft123"}

# ---- Step 2: Define the State for LangGraph ----
class State(TypedDict):
    messages: Annotated[list, add_messages]
    agent_state: str  # Track the current state of the agent ("WAIT", "RUN", or "ERROR")

# Initialize the StateGraph
graph_builder = StateGraph(State)
llm = ChatOpenAI(model="gpt-4")

# ---- Step 3: Define Agent Functions with State Handling ----
def draft_agent(state: State):
    """Simulates a Draft Agent generating a draft based on prompts."""
    state["agent_state"] = "RUN"  # Update agent state to RUN on function entry
    try:
        draft_prompt = get_latest_prompts_from_sanity()
        result = {"messages": [llm.invoke([("system", draft_prompt)])]}
        state["agent_state"] = "WAIT"  # Update state to WAIT on successful exit
        return result
    except Exception as e:
        state["agent_state"] = "ERROR"  # Update state to ERROR on exception
        print(f"Draft Agent encountered an error: {e}")
        return state

def icp_agent(state: State):
    """Simulates the ICP Agent validating the generated draft."""
    state["agent_state"] = "RUN"
    try:
        print("ICP Agent: Validating the draft...")
        state["agent_state"] = "WAIT"
        return {"messages": [("system", "Draft validated successfully for ICP.")]}
    except Exception as e:
        state["agent_state"] = "ERROR"
        print(f"ICP Agent encountered an error: {e}")
        return state

def critic_agent(state: State):
    """Simulates the Critic Agent providing feedback on the draft."""
    state["agent_state"] = "RUN"
    try:
        print("Critic Agent: Refining the draft...")
        state["agent_state"] = "WAIT"
        return {"messages": [("system", "Refined draft with Critic feedback.")]}
    except Exception as e:
        state["agent_state"] = "ERROR"
        print(f"Critic Agent encountered an error: {e}")
        return state

def cta_agent(state: State):
    """Simulates the CTA Agent generating a CTA based on the refined draft."""
    state["agent_state"] = "RUN"
    try:
        print("CTA Agent: Generating CTA...")
        state["agent_state"] = "WAIT"
        return {"messages": [("system", "Download your guide now and escape burnout!")]}
    except Exception as e:
        state["agent_state"] = "ERROR"
        print(f"CTA Agent encountered an error: {e}")
        return state

# XAgent Stub Function (Does Nothing)
def x_agent(_refined_draft, _cta):
    """XAgent stub that does nothing."""
    pass

# ---- Step 4: Integrate Agent Functions into the LangGraph Framework ----
# Each agent is added as a separate node in the state graph
graph_builder.add_node("draft_agent", draft_agent)
graph_builder.add_node("icp_agent", icp_agent)
graph_builder.add_node("critic_agent", critic_agent)
graph_builder.add_node("cta_agent", cta_agent)

# Set up the graph's entry and finish points
graph_builder.set_entry_point("draft_agent")
graph_builder.set_finish_point("cta_agent")

# Compile the graph
graph = graph_builder.compile()

# ---- Step 5: Main Loop to Execute the Workflow ----
def main_loop():
    print("Starting main loop...")

    # Initial input prompt to simulate a user query (modify as needed)
    user_input = "Generate a draft about tech burnout."

    # Initialize the 'value' variable to handle scope issues and track agent states
    value = {"messages": [("system", "")], "agent_state": "WAIT"}  # Placeholder with state tracking

    # Step 1: Generate initial draft using Draft Agent
    print("Running Draft Agent...")
    for event in graph.stream({"messages": [("user", user_input)], "agent_state": "RUN"}):
        for value in event.values():
            print("DraftAgent Output:", value["messages"][-1][1])  # Access the text content directly

    # Step 2: ICP Agent validates the draft
    print("Running ICP Agent...")
    if value:
        for event in graph.stream({"messages": [("system", value["messages"][-1][1])], "agent_state": "RUN"}):
            for value in event.values():
                print("ICPAgent Output:", value["messages"][-1][1])

    # Step 3: Critic Agent refines the draft
    print("Running Critic Agent...")
    if value:
        for event in graph.stream({"messages": [("system", value["messages"][-1][1])], "agent_state": "RUN"}):
            for value in event.values():
                print("CriticAgent Output:", value["messages"][-1][1])

    # Step 4: CTA Agent generates the call-to-action
    print("Running CTA Agent...")
    refined_draft = ""
    if value:
        for event in graph.stream({"messages": [("system", value["messages"][-1][1])], "agent_state": "RUN"}):
            for value in event.values():
                refined_draft = value["messages"][-1][1]
                print("CTAAgent Output:", refined_draft)

    # Step 5: Insert into Sanity.io for Substack and X
    print("Inserting drafts into Sanity.io for review...")
    insert_draft_into_sanity(refined_draft, platform='Substack')
    insert_draft_into_sanity(refined_draft, platform='X')

    # Human review and approval would occur here (simulate with a print statement)
    print("Drafts ready for human review in Sanity.io")

    # Step 6: XAgent placeholder
    x_agent(refined_draft, "Placeholder CTA")

# Run the main loop
if __name__ == "__main__":
    main_loop()
