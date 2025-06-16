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
        # 準備輸入信息
        input_data = {
            "task": state.get("current_task", ""),
            "research_results": state.get("research_results", []),
            "previous_analysis": state.get("analysis_results", [])
        }
        
        # 獲取分析結果
        result = self.chain.invoke({"input": json.dumps(input_data, ensure_ascii=False)})
        
        # 返回新狀態
        return {
            "analysis_results": [result],
            "current_agent": "analyst",
            "next_agent": "supervisor"
        } 