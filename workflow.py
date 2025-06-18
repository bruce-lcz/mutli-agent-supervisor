from typing import Dict, List, Any, TypedDict, Annotated, Sequence
from langgraph.graph import Graph, END
from langgraph.prebuilt import ToolNode
from agents.supervisor import SupervisorAgent
from agents.researcher import ResearcherAgent
from agents.analyst import AnalystAgent
import json
import time
from datetime import datetime

# 定義狀態類型
class AgentState(TypedDict):
    task_assignments: List[Dict[str, Any]]
    research_results: List[Dict[str, Any]]
    analysis_results: List[Dict[str, Any]]
    execution_times: List[Dict[str, Any]]
    agent_sequence: List[str]
    current_agent: str
    next_agent: str
    current_task: str
    final_decision: str
    iteration: int

def create_workflow() -> Graph:
    # 初始化 agents
    supervisor = SupervisorAgent()
    researcher = ResearcherAgent()
    analyst = AnalystAgent()
    
    # 創建工作流圖
    workflow = Graph()
    
    def validate_state(state: AgentState) -> bool:
        """驗證狀態是否有效"""
        required_fields = [
            "task_assignments", "research_results", "analysis_results",
            "execution_times", "agent_sequence", "current_agent",
            "next_agent", "current_task", "final_decision", "iteration"
        ]
        return all(field in state for field in required_fields)
    
    # 定義節點
    def supervisor_node(state: AgentState) -> AgentState:
        if not validate_state(state):
            print("警告: 無效的狀態進入 supervisor_node")
            return state
            
        start_time = time.time()
        current_time = datetime.now().strftime("%H:%M:%S")
        
        result = supervisor.evaluate_and_assign(state)
        if result.get("task_assignments"):
            state["task_assignments"].extend(result["task_assignments"])
        state["next_agent"] = result.get("next_agent", "end")
        state["current_task"] = result.get("current_task", state["current_task"])
        state["final_decision"] = result.get("final_decision", "")
        
        # 更新執行時間和序列
        end_time = time.time()
        execution_time = end_time - start_time
        state["execution_times"].append({
            "iteration": state["iteration"],
            "agent": "supervisor",
            "start_time": current_time,
            "execution_time": f"{execution_time:.2f}秒"
        })
        state["agent_sequence"].append("supervisor")
        state["iteration"] += 1
        
        return state
    
    def researcher_node(state: AgentState) -> AgentState:
        if not validate_state(state):
            print("警告: 無效的狀態進入 researcher_node")
            return state
            
        start_time = time.time()
        current_time = datetime.now().strftime("%H:%M:%S")
        
        result = researcher.research(state)
        if result.get("research_results"):
            state["research_results"].extend(result["research_results"])
        state["next_agent"] = result.get("next_agent", "supervisor")
        
        # 更新執行時間和序列
        end_time = time.time()
        execution_time = end_time - start_time
        state["execution_times"].append({
            "iteration": state["iteration"],
            "agent": "researcher",
            "start_time": current_time,
            "execution_time": f"{execution_time:.2f}秒"
        })
        state["agent_sequence"].append("researcher")
        state["iteration"] += 1
        
        return state
    
    def analyst_node(state: AgentState) -> AgentState:
        if not validate_state(state):
            print("警告: 無效的狀態進入 analyst_node")
            return state
            
        start_time = time.time()
        current_time = datetime.now().strftime("%H:%M:%S")
        
        result = analyst.analyze(state)
        if result.get("analysis_results"):
            state["analysis_results"].extend(result["analysis_results"])
        state["next_agent"] = result.get("next_agent", "supervisor")
        
        # 更新執行時間和序列
        end_time = time.time()
        execution_time = end_time - start_time
        state["execution_times"].append({
            "iteration": state["iteration"],
            "agent": "analyst",
            "start_time": current_time,
            "execution_time": f"{execution_time:.2f}秒"
        })
        state["agent_sequence"].append("analyst")
        state["iteration"] += 1
        
        return state
    
    # 添加節點到工作流
    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("analyst", analyst_node)
    
    # 定義條件邊
    def to_researcher(state: AgentState) -> bool:
        return state["next_agent"] == "researcher"
    
    def to_analyst(state: AgentState) -> bool:
        return state["next_agent"] == "analyst"
    
    def to_end(state: AgentState) -> bool:
        return state["next_agent"] == "end"
    
    def to_supervisor(state: AgentState) -> bool:
        return state["next_agent"] == "supervisor"
    
    # 添加條件邊
    workflow.add_conditional_edges(
        "supervisor",
        {
            "researcher": to_researcher,
            "analyst": to_analyst,
            END: to_end
        }
    )
    
    workflow.add_conditional_edges(
        "researcher",
        {
            "supervisor": to_supervisor
        }
    )
    
    workflow.add_conditional_edges(
        "analyst",
        {
            "supervisor": to_supervisor
        }
    )
    
    # 設置入口點
    workflow.set_entry_point("supervisor")
    
    # 編譯工作流
    app = workflow.compile()
    
    # 包裝工作流以確保返回最終狀態
    def wrapped_workflow(state: AgentState) -> AgentState:
        try:
            result = app.invoke(state)
            
            # 如果結果為 None，檢查狀態轉換
            if result is None:
                # 如果應該轉換到 researcher 但沒有成功，手動更新狀態
                if state['next_agent'] == 'researcher':
                    new_state = researcher_node(state)
                    # 遞歸調用以繼續工作流
                    return wrapped_workflow(new_state)
                # 如果應該轉換到 analyst 但沒有成功，手動更新狀態
                elif state['next_agent'] == 'analyst':
                    new_state = analyst_node(state)
                    # 遞歸調用以繼續工作流
                    return wrapped_workflow(new_state)
                # 如果應該結束但沒有成功，返回當前狀態
                elif state['next_agent'] == 'end':
                    return state
                
                return state
            return result
        except Exception as e:
            print(f"工作流執行錯誤: {str(e)}")
            return state
    
    return wrapped_workflow

def create_initial_state(task: str) -> AgentState:
    """創建初始狀態"""
    return {
        "task_assignments": [],
        "research_results": [],
        "analysis_results": [],
        "execution_times": [],
        "agent_sequence": [],
        "current_agent": "supervisor",
        "next_agent": "supervisor",
        "current_task": task,
        "final_decision": "",
        "iteration": 1
    } 