from typing import Dict, List, Any, TypedDict, Annotated
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel, Field

class AgentState(TypedDict):
    """State of the agent system."""
    messages: List[Dict[str, Any]]
    current_agent: str
    next_agent: str
    task: str
    research_results: List[str]
    analysis_results: List[str]
    final_decision: str

class BaseAgent:
    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=0.7
        )
        self.parser = StrOutputParser()

class Researcher(BaseAgent):
    """Agent responsible for gathering and analyzing information."""
    
    def __init__(self):
        super().__init__()
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a Research Agent. Your role is to:
            1. Gather relevant information about the given task
            2. Analyze the information
            3. Provide detailed findings
            
            Be thorough and objective in your research."""),
            ("human", "{task}")
        ])
        
    def run(self, state: AgentState) -> AgentState:
        chain = self.prompt | self.llm | self.parser
        research_results = chain.invoke({"task": state["task"]})
        
        state["research_results"].append(research_results)
        state["current_agent"] = "researcher"
        state["next_agent"] = "analyst"
        
        return state

class Analyst(BaseAgent):
    """Agent responsible for processing and summarizing information."""
    
    def __init__(self):
        super().__init__()
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an Analysis Agent. Your role is to:
            1. Review the research findings
            2. Identify key patterns and insights
            3. Provide a clear summary of the analysis
            
            Focus on extracting actionable insights."""),
            ("human", "Research findings: {research_results}")
        ])
        
    def run(self, state: AgentState) -> AgentState:
        chain = self.prompt | self.llm | self.parser
        analysis_results = chain.invoke({
            "research_results": "\n".join(state["research_results"])
        })
        
        state["analysis_results"].append(analysis_results)
        state["current_agent"] = "analyst"
        state["next_agent"] = "decision_maker"
        
        return state

class DecisionMaker(BaseAgent):
    """Agent responsible for making final decisions."""
    
    def __init__(self):
        super().__init__()
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a Decision Making Agent. Your role is to:
            1. Review the analysis
            2. Consider all factors
            3. Make a clear, actionable decision
            
            Be decisive and provide clear reasoning for your decision."""),
            ("human", "Analysis results: {analysis_results}")
        ])
        
    def run(self, state: AgentState) -> AgentState:
        chain = self.prompt | self.llm | self.parser
        decision = chain.invoke({
            "analysis_results": "\n".join(state["analysis_results"])
        })
        
        state["final_decision"] = decision
        state["current_agent"] = "decision_maker"
        state["next_agent"] = "end"
        
        return state 