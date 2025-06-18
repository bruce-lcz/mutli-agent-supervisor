from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
import json

class SupervisorAgent:
    def __init__(self, model_name: str = "gpt-4-turbo-preview"):
        self.llm = ChatOpenAI(model_name=model_name, temperature=0)
        self.chain = self._create_chain()
    
    def _create_chain(self):
        prompt = ChatPromptTemplate.from_messages([
            ("system", """你是一個Agent監督者，負責協調和管理其他Agent的工作。
            你的職責包括：
            1. 分析任務需求並決定需要哪些Agent參與
            2. 分配任務給合適的Agent
            3. 評估Agent的執行結果
            4. 決定是否需要更多迭代或任務已完成
            
            請根據以下信息做出決策：
            - 當前任務狀態
            - 已完成的任務
            - Agent的執行結果
            - 是否需要更多信息或分析
            
            你必須以嚴格的 JSON 格式返回決策，格式如下：
            {{
                "next_agent": "researcher" | "analyst" | "end",
                "task": "具體任務描述",
                "is_complete": true/false,
                "final_decision": "如果完成，提供最終決策"
            }}
            
            注意：
            1. 必須返回有效的 JSON 格式
            2. next_agent 只能是 "researcher"、"analyst" 或 "end"
            3. is_complete 必須是 true 或 false
            4. 如果 is_complete 為 true，必須提供 final_decision
            5. task 必須是具體的任務描述
            
            示例輸出：
            對於新任務：
            {{
                "next_agent": "researcher",
                "task": "收集關於咖啡店營運成本的信息",
                "is_complete": false,
                "final_decision": ""
            }}
            
            對於完成的分析：
            {{
                "next_agent": "end",
                "task": "完成最終分析報告",
                "is_complete": true,
                "final_decision": "根據分析，咖啡店的每日營運成本約為5000元，主要支出包括租金、人工和原材料。建議通過優化人員排班和供應鏈管理來降低成本。"
            }}"""),
            ("human", "{input}")
        ])
        
        return prompt | self.llm | StrOutputParser()
    
    def evaluate_and_assign(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """評估當前狀態並決定下一步行動"""
        # 準備輸入信息
        input_data = {
            "current_task": state.get("current_task", ""),
            "task_assignments": state.get("task_assignments", []),
            "research_results": state.get("research_results", []),
            "analysis_results": state.get("analysis_results", [])
        }
        
        # 獲取監督者的決策
        decision = self.chain.invoke({"input": json.dumps(input_data, ensure_ascii=False)})
        
        try:
            # 解析決策
            decision_data = json.loads(decision)
            
            # 驗證決策格式
            if not isinstance(decision_data, dict):
                raise ValueError("決策必須是 JSON 對象")
            
            required_fields = ["next_agent", "task", "is_complete"]
            for field in required_fields:
                if field not in decision_data:
                    raise ValueError(f"缺少必要字段: {field}")
            
            if decision_data["next_agent"] not in ["researcher", "analyst", "end"]:
                raise ValueError("next_agent 必須是 researcher、analyst 或 end")
            
            if not isinstance(decision_data["is_complete"], bool):
                raise ValueError("is_complete 必須是布爾值")
            
            if decision_data["is_complete"] and not decision_data.get("final_decision"):
                raise ValueError("當 is_complete 為 true 時，必須提供 final_decision")
            
            # 返回新狀態
            return {
                "task_assignments": [{
                    "iteration": len(state.get("task_assignments", [])) + 1,
                    "agent": decision_data["next_agent"],
                    "task": decision_data["task"]
                }],
                "next_agent": decision_data["next_agent"],
                "current_task": decision_data["task"],
                "final_decision": decision_data.get("final_decision", ""),
                "current_agent": "supervisor"
            }
            
        except (json.JSONDecodeError, ValueError) as e:
            # 如果解析失敗，返回錯誤信息
            error_msg = f"監督者決策解析失敗: {str(e)}"
            print(f"\n錯誤: {error_msg}")
            return {
                "task_assignments": [],
                "next_agent": "end",
                "current_task": state.get("current_task", ""),
                "final_decision": error_msg,
                "current_agent": "supervisor"
            } 