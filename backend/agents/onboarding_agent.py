"""
Onboarding Agent for CogniFlow.

LangGraph-based agent for assisting with seller onboarding tasks.
"""

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from langchain_ollama import ChatOllama


class AgentState(TypedDict):
    """State maintained throughout the agent conversation."""
    messages: list[dict]
    seller_id: int | None
    current_step: str
    documents: list[dict]


def create_llm() -> ChatOllama:
    """Create the Ollama LLM instance."""
    return ChatOllama(
        model="llama3.2",
        temperature=0.7,
    )


def greet_node(state: AgentState) -> AgentState:
    """Initial greeting and context gathering."""
    llm = create_llm()
    
    system_prompt = """You are CogniFlow, an AI assistant helping Account Managers 
    with seller onboarding. Be helpful, professional, and guide users through 
    the onboarding process. Keep responses concise."""
    
    messages = state["messages"]
    
    # Get last user message
    user_message = messages[-1]["content"] if messages else "Hello"
    
    response = llm.invoke([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ])
    
    new_messages = messages + [{"role": "assistant", "content": response.content}]
    
    return {
        **state,
        "messages": new_messages,
        "current_step": "greeted"
    }


def route_message(state: AgentState) -> Literal["greet", "end"]:
    """Route to appropriate node based on state."""
    # For now, simple routing - always greet and end
    if state.get("current_step") == "greeted":
        return "end"
    return "greet"


def build_agent() -> StateGraph:
    """Build and compile the LangGraph agent."""
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("greet", greet_node)
    
    # Add edges
    workflow.set_entry_point("greet")
    workflow.add_edge("greet", END)
    
    return workflow.compile()


# Compiled agent instance
agent = build_agent()


def invoke_agent(
    message: str,
    seller_id: int | None = None,
    history: list[dict] | None = None
) -> dict:
    """
    Invoke the onboarding agent with a user message.
    
    Args:
        message: User's message
        seller_id: Optional seller context
        history: Optional conversation history
        
    Returns:
        dict with response and updated state
    """
    messages = history or []
    messages.append({"role": "user", "content": message})
    
    initial_state: AgentState = {
        "messages": messages,
        "seller_id": seller_id,
        "current_step": "start",
        "documents": []
    }
    
    result = agent.invoke(initial_state)
    
    # Extract assistant response
    assistant_messages = [
        m for m in result["messages"] 
        if m.get("role") == "assistant"
    ]
    
    response = assistant_messages[-1]["content"] if assistant_messages else ""
    
    return {
        "response": response,
        "messages": result["messages"],
        "current_step": result["current_step"]
    }
