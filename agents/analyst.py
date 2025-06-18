from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
import json

class AnalystAgent:
    def __init__(self, model_name: str = "gpt-4-turbo-preview"):
        self.llm = ChatOpenAI(model_name=model_name, temperature=0)
        self.chain = self._create_chain()
    
    def _create_chain(self):
        prompt = ChatPromptTemplate.from_messages([
            ("system", """你是一個分析師Agent，負責分析和評估信息。
            你的職責包括：
            1. 分析研究結果
            2. 評估信息的可靠性和相關性
            3. 提供深入的分析見解
            4. 識別關鍵模式和趨勢
            
            請確保你的分析：
            - 邏輯清晰
            - 基於事實
            - 提供有價值的見解
            - 幫助決策制定"""),
            ("human", "{input}")
        ])
        
        return prompt | self.llm | StrOutputParser()
    
    def analyze(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """執行分析任務"""
        try:
            # 準備輸入信息
            input_data = {
                "task": state.get("current_task", ""),
                "research_results": state.get("research_results", []),
                "previous_analysis": state.get("analysis_results", [])
            }
            
            # 獲取分析結果
            result = self.chain.invoke({"input": json.dumps(input_data, ensure_ascii=False)})
            
            # 返回新狀態，保持原有狀態的完整性
            return {
                "task_assignments": state.get("task_assignments", []),
                "research_results": state.get("research_results", []),
                "analysis_results": state.get("analysis_results", []) + [result],
                "execution_times": state.get("execution_times", []),
                "agent_sequence": state.get("agent_sequence", []),
                "current_agent": "analyst",
                "next_agent": "supervisor",
                "current_task": state.get("current_task", ""),
                "final_decision": state.get("final_decision", ""),
                "iteration": state.get("iteration", 1)
            }
        except Exception as e:
            print(f"\nAnalyst 錯誤: {str(e)}")
            # 返回錯誤狀態，但確保工作流可以繼續
            return {
                "task_assignments": state.get("task_assignments", []),
                "research_results": state.get("research_results", []),
                "analysis_results": state.get("analysis_results", []) + [f"分析過程中發生錯誤: {str(e)}"],
                "execution_times": state.get("execution_times", []),
                "agent_sequence": state.get("agent_sequence", []),
                "current_agent": "analyst",
                "next_agent": "supervisor",
                "current_task": state.get("current_task", ""),
                "final_decision": state.get("final_decision", ""),
                "iteration": state.get("iteration", 1)
            } 