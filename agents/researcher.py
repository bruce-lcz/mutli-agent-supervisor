from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
import json

class ResearcherAgent:
    def __init__(self, model_name: str = "gpt-4-turbo-preview"):
        self.llm = ChatOpenAI(model_name=model_name, temperature=0)
        self.chain = self._create_chain()
    
    def _create_chain(self):
        prompt = ChatPromptTemplate.from_messages([
            ("system", """你是一個研究員Agent，負責收集和分析信息。
            你的職責包括：
            1. 根據任務需求收集相關信息
            2. 整理和組織收集到的信息
            3. 提供清晰的研究結果
            
            請確保你的研究結果：
            - 與任務相關
            - 信息準確
            - 結構清晰
            - 易於理解"""),
            ("human", "{input}")
        ])
        
        return prompt | self.llm | StrOutputParser()
    
    def research(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """執行研究任務"""
        try:
            # 準備輸入信息
            input_data = {
                "task": state.get("current_task", ""),
                "previous_research": state.get("research_results", [])
            }
            
            # 獲取研究結果
            result = self.chain.invoke({"input": json.dumps(input_data, ensure_ascii=False)})
            
            # 返回新狀態，保持原有狀態的完整性
            return {
                "task_assignments": state.get("task_assignments", []),
                "research_results": state.get("research_results", []) + [result],
                "analysis_results": state.get("analysis_results", []),
                "execution_times": state.get("execution_times", []),
                "agent_sequence": state.get("agent_sequence", []),
                "current_agent": "researcher",
                "next_agent": "supervisor",
                "current_task": state.get("current_task", ""),
                "final_decision": state.get("final_decision", ""),
                "iteration": state.get("iteration", 1)
            }
        except Exception as e:
            print(f"\nResearcher 錯誤: {str(e)}")
            # 返回錯誤狀態，但確保工作流可以繼續
            return {
                "task_assignments": state.get("task_assignments", []),
                "research_results": state.get("research_results", []) + [f"研究過程中發生錯誤: {str(e)}"],
                "analysis_results": state.get("analysis_results", []),
                "execution_times": state.get("execution_times", []),
                "agent_sequence": state.get("agent_sequence", []),
                "current_agent": "researcher",
                "next_agent": "supervisor",
                "current_task": state.get("current_task", ""),
                "final_decision": state.get("final_decision", ""),
                "iteration": state.get("iteration", 1)
            } 