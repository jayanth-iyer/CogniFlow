"""
Onboarding Agent for CogniFlow.

LangGraph-based agent for assisting with seller onboarding tasks.
Now includes LangFuse tracing and database tools.
"""

from typing import TypedDict, Literal, Annotated
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage
try:
    from langfuse.callback import CallbackHandler
except ImportError:
    CallbackHandler = None
from sqlmodel import Session, select, func
import os

from database import engine
from models.document import Document
from models.seller import Seller

class AgentState(TypedDict):
    """State maintained throughout the agent conversation."""
    messages: list[BaseMessage]
    seller_id: int | None

@tool
def check_document_status(seller_id: int | None = None) -> str:
    """
    Check the status and count of uploaded documents for a seller.
    If no seller_id is provided, checks global stats (for demo purposes).
    """
    try:
        with Session(engine) as session:
            if seller_id:
                statement = select(Document).where(Document.seller_id == seller_id)
                docs = session.exec(statement).all()
                if not docs:
                    return f"No documents found for seller ID {seller_id}."
                status_summary = [f"{d.filename}: {d.status}" for d in docs]
                return f"Found {len(docs)} documents:\n" + "\n".join(status_summary)
            else:
                # Demo mode: count all documents
                count = session.exec(select(func.count(Document.id))).one()
                return f"There are currently {count} documents in the system."
    except Exception as e:
        return f"Error checking documents: {str(e)}"

@tool
def search_sellers(name_query: str) -> str:
    """
    Search for sellers by name or business name.
    """
    try:
        with Session(engine) as session:
            statement = select(Seller).where(
                (Seller.name.contains(name_query)) | 
                (Seller.business_name.contains(name_query))
            )
            sellers = session.exec(statement).all()
            if not sellers:
                return f"No sellers found matching '{name_query}'."
            
            results = [f"ID: {s.id}, Business: {s.business_name}, Name: {s.name}, Status: {s.status}" for s in sellers]
            return f"Found {len(sellers)} sellers:\n" + "\n".join(results)
    except Exception as e:
        return f"Error searching sellers: {str(e)}"

@tool
def analyze_document(document_id: int) -> str:
    """
    Analyze a document by ID to extract key information (Simulated).
    In a real system, this would use OCR/LLM on the file content.
    """
    try:
        with Session(engine) as session:
            doc = session.get(Document, document_id)
            if not doc:
                return f"Document ID {document_id} not found."
            
            # Simulated analysis result
            analysis = f"Analysis for {doc.filename}:\n"
            analysis += f"- Status: {doc.status}\n"
            analysis += f"- Type: {doc.filename.split('.')[-1].upper()}\n"
            analysis += "- Content Validity: Verified (Simulated)\n"
            analysis += "- Missing Fields: None detected"
            
            return analysis
    except Exception as e:
        return f"Error analyzing document: {str(e)}"

def create_llm():
    """Create the Ollama LLM instance with optional LangFuse callback."""
    # Initialize LangFuse handler if keys are present and module is available
    callbacks = []
    if CallbackHandler and os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY"):
        callbacks.append(CallbackHandler())

    return ChatOllama(
        model="llama3.2",
        base_url="http://127.0.0.1:11434",
        temperature=0.7,
        callbacks=callbacks
    )

def agent_node(state: AgentState):
    """Main agent node that calls the LLM with tools."""
    llm = create_llm()
    
    # Bind tools to the LLM
    tools = [check_document_status, search_sellers, analyze_document]
    llm_with_tools = llm.bind_tools(tools)
    
    messages = state["messages"]
    
    # Ensure system prompt is present
    if not isinstance(messages[0], SystemMessage):
        system_prompt = SystemMessage(content="""You are CogniFlow, an AI assistant helping Account Managers 
        with seller onboarding. You have access to tools to check document status, search for sellers, and analyze documents.
        If asked about documents, use check_document_status or analyze_document.
        If asked to find a seller, use search_sellers.
        Be helpful, professional, and concise.""")
        messages = [system_prompt] + messages
    
    response = llm_with_tools.invoke(messages)
    
    return {"messages": [response]}

def should_continue(state: AgentState) -> Literal["tools", "end"]:
    """Determine if the agent should call a tool or end."""
    last_message = state["messages"][-1]
    
    if last_message.tool_calls:
        return "tools"
    return "end"

def build_agent() -> StateGraph:
    """Build and compile the LangGraph agent."""
    workflow = StateGraph(AgentState)
    
    # Define Tools
    # Define Tools
    tools = [check_document_status, search_sellers, analyze_document]
    tool_node = ToolNode(tools)
    
    # Add nodes
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tool_node)
    
    # Add edges
    workflow.set_entry_point("agent")
    
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            "end": END
        }
    )
    
    workflow.add_edge("tools", "agent")
    
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
    """
    # Convert dict history to BaseMessages if needed (simplified for now)
    # Ideally reuse existing conversion logic or standard LangChain adapters
    
    # For this simple implementation, we just construct the input message list
    input_messages = []
    
    if history:
        for msg in history:
            if msg["role"] == "user":
                input_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                input_messages.append(AIMessage(content=msg["content"]))
                
    input_messages.append(HumanMessage(content=message))
    
    initial_state: AgentState = {
        "messages": input_messages,
        "seller_id": seller_id
    }
    
    # Run the graph
    result = agent.invoke(initial_state)
    
    # Get the last message
    last_message = result["messages"][-1]
    response_content = last_message.content if isinstance(last_message, AIMessage) else str(last_message)
    
    # Return details for API
    return {
        "response": response_content,
        "messages": [
            {"role": "user" if isinstance(m, HumanMessage) else "assistant" if isinstance(m, AIMessage) else "system", 
             "content": m.content} 
            for m in result["messages"]
        ],
        "current_step": "onboarding" # simplified for now
    }
