import os
from typing import Dict, List, Any, TypedDict, Annotated
from langgraph.graph import StateGraph, END
from agents import AgentState, Researcher, Analyst, DecisionMaker
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_agent_graph():
    """Create the agent workflow graph."""
    # Initialize agents
    researcher = Researcher()
    analyst = Analyst()
    decision_maker = DecisionMaker()
    
    # Create the graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("researcher", researcher.run)
    workflow.add_node("analyst", analyst.run)
    workflow.add_node("decision_maker", decision_maker.run)
    
    # Add edges
    workflow.add_edge("researcher", "analyst")
    workflow.add_edge("analyst", "decision_maker")
    workflow.add_edge("decision_maker", END)
    
    # Set entry point
    workflow.set_entry_point("researcher")
    
    return workflow.compile()

def main():
    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("Please set OPENAI_API_KEY environment variable")
    
    # Create the agent graph
    agent_graph = create_agent_graph()
    
    # Example task
    task = """
    Analyze the current trends in artificial intelligence and provide recommendations 
    for a small business looking to implement AI solutions.
    """
    
    # Initialize state
    initial_state = {
        "messages": [],
        "current_agent": "",
        "next_agent": "researcher",
        "task": task,
        "research_results": [],
        "analysis_results": [],
        "final_decision": ""
    }
    
    # Run the workflow
    logger.info("Starting agent workflow...")
    final_result = agent_graph.invoke(initial_state)
    
    # Print results
    print("\n=== Research Results ===")
    for i, research in enumerate(final_result["research_results"], 1):
        print(f"\nResearch {i}:")
        print(research)
    
    print("\n=== Analysis Results ===")
    for i, analysis in enumerate(final_result["analysis_results"], 1):
        print(f"\nAnalysis {i}:")
        print(analysis)
    
    print("\n=== Final Decision ===")
    print(final_result["final_decision"])

if __name__ == "__main__":
    main() 