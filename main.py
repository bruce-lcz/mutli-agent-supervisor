from typing import Dict, List, Any, TypedDict
from agents.analyst import AnalystAgent
from agents.researcher import ResearcherAgent
from agents.supervisor import SupervisorAgent
import logging
from dotenv import load_dotenv
import time
from datetime import datetime
import json
import os

# 加載環境變量
load_dotenv()

# 檢查 API key
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("請在 .env 文件中設置 OPENAI_API_KEY 環境變量")

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WorkflowState:
    def __init__(self, task: str):
        self.task_assignments = []
        self.research_results = []
        self.analysis_results = []
        self.execution_times = []
        self.agent_sequence = []
        self.current_agent = "supervisor"
        self.next_agent = "supervisor"
        self.current_task = task
        self.final_decision = ""

def main():
    # 初始化Agent
    researcher = ResearcherAgent()
    analyst = AnalystAgent()
    supervisor = SupervisorAgent()
    
    # 獲取用戶輸入的任務
    print("\n=== 多Agent系統 ===")
    print("請輸入您想要分析的任務（輸入 'quit' 退出）：")
    print("例如：分析一家咖啡店的每日營運成本")
    print("     設計一個智能家居系統")
    print("     規劃一個為期3個月的減重計劃")
    print("     評估公司是否應該將業務遷移到雲端")
    print("\n您的任務：")
    
    task = input().strip()
    
    if task.lower() == 'quit':
        print("程序已退出")
        return
    
    # 初始化狀態
    state = WorkflowState(task)
    
    # 設置最大迭代次數以防止無限循環
    max_iterations = 10
    current_iteration = 0
    
<<<<<<< Updated upstream
    while current_iteration < max_iterations:
        current_iteration += 1
        print(f"\n=== 迭代 {current_iteration} ===")
        
        # 記錄開始時間
        start_time = time.time()
        current_time = datetime.now().strftime("%H:%M:%S")
        
        # 根據當前Agent執行相應的操作
        if state.current_agent == "supervisor":
            result = supervisor.evaluate_and_assign(state.__dict__)
            if result.get("task_assignments"):
                state.task_assignments.extend(result["task_assignments"])
            state.next_agent = result.get("next_agent", "end")
            state.current_task = result.get("current_task", state.current_task)
            state.final_decision = result.get("final_decision", "")
            
        elif state.current_agent == "researcher":
            result = researcher.research(state.__dict__)
            if result.get("research_results"):
                state.research_results.extend(result["research_results"])
            state.next_agent = result.get("next_agent", "supervisor")
            
        elif state.current_agent == "analyst":
            result = analyst.analyze(state.__dict__)
            if result.get("analysis_results"):
                state.analysis_results.extend(result["analysis_results"])
            state.next_agent = result.get("next_agent", "supervisor")
        
        # 記錄執行時間
        end_time = time.time()
        execution_time = end_time - start_time
        
        # 記錄執行信息
        execution_info = {
            "iteration": current_iteration,
            "agent": state.current_agent,
            "start_time": current_time,
            "execution_time": f"{execution_time:.2f}秒"
        }
        state.execution_times.append(execution_info)
        state.agent_sequence.append(state.current_agent)
        
        # 更新當前Agent
        state.current_agent = state.next_agent
        
        # 檢查是否完成
        if state.next_agent == "end":
            print("\n=== 分析完成 ===")
            break
        
        # 如果達到最大迭代次數
        if current_iteration == max_iterations:
            print("\n=== 達到最大迭代次數，強制結束 ===")
            break
    
    # 整理並顯示最終結果
    print("\n" + "="*50)
    print("最終分析報告".center(50))
    print("="*50)
    
    # 1. 執行摘要
    print("\n【執行摘要】")
    print(f"總迭代次數: {len(state.agent_sequence)}")
    print(f"總研究次數: {len(state.research_results)}")
    print(f"總分析次數: {len(state.analysis_results)}")
    print(f"總執行時間: {sum(float(info['execution_time'].replace('秒', '')) for info in state.execution_times):.2f}秒")
    
    # 2. 執行順序
    print("\n【執行順序】")
    sequence = " -> ".join(state.agent_sequence)
    print(sequence)
    
    # 3. 最後一次迭代的詳細信息
    print("\n【最後一次迭代詳情】")
    if state.task_assignments:
        last_iteration = state.task_assignments[-1]
        print(f"Agent: {last_iteration['agent']}")
        print(f"分配任務: {last_iteration['task']}")
    
    # 4. 最終決策
    print("\n【最終決策】")
    print(state.final_decision)
    
    # 5. 完整執行記錄（可選）
    print("\n" + "="*50)
    print("完整執行記錄（按Enter鍵查看）".center(50))
    print("="*50)
    input()
    
    print("\n【任務分配記錄】")
    for assignment in state.task_assignments:
        print(f"\n迭代 {assignment['iteration']}:")
        print(f"Agent: {assignment['agent']}")
        print(f"分配任務: {assignment['task']}")
    
    print("\n【執行時間記錄】")
    for info in state.execution_times:
        print(f"\n步驟 {info['iteration']}:")
        print(f"Agent: {info['agent']}")
        print(f"開始時間: {info['start_time']}")
        print(f"執行時間: {info['execution_time']}")
    
    print("\n【研究結果】")
    for i, research in enumerate(state.research_results, 1):
        print(f"\n研究 {i}:")
        print(research)
    
    print("\n【分析結果】")
    for i, analysis in enumerate(state.analysis_results, 1):
        print(f"\n分析 {i}:")
        print(analysis)
=======
    # 執行工作流
    print("\n開始執行工作流...")
    try:
        # 直接調用工作流函數
        final_state = workflow(initial_state)
        
        if final_state is None:
            print("\n工作流執行失敗，未返回最終狀態")
            return
        
        # 整理並顯示最終結果
        print("\n" + "="*50)
        print("最終分析報告".center(50))
        print("="*50)
        
        # 1. 執行摘要
        print("\n【執行摘要】")
        print(f"總迭代次數: {len(final_state['agent_sequence'])}")
        print(f"總研究次數: {len(final_state['research_results'])}")
        print(f"總分析次數: {len(final_state['analysis_results'])}")
        print(f"總執行時間: {sum(float(info['execution_time'].replace('秒', '')) for info in final_state['execution_times']):.2f}秒")
        
        # 2. 執行順序
        print("\n【執行順序】")
        sequence = " -> ".join(final_state['agent_sequence'])
        print(sequence)
        
        # 3. 最後一次迭代的詳細信息
        print("\n【最後一次迭代詳情】")
        if final_state['task_assignments']:
            last_iteration = final_state['task_assignments'][-1]
            print(f"Agent: {last_iteration['agent']}")
            print(f"分配任務: {last_iteration['task']}")
        
        # 4. 最終決策
        print("\n【最終決策】")
        print(final_state['final_decision'])
        
        # 5. 完整執行記錄
        print("\n" + "="*50)
        print("完整執行記錄".center(50))
        print("="*50)
        
        print("\n【任務分配記錄】")
        for assignment in final_state['task_assignments']:
            print(f"\n迭代 {assignment['iteration']}:")
            print(f"Agent: {assignment['agent']}")
            print(f"分配任務: {assignment['task']}")
        
        print("\n【執行時間記錄】")
        for info in final_state['execution_times']:
            print(f"\n步驟 {info['iteration']}:")
            print(f"Agent: {info['agent']}")
            print(f"開始時間: {info['start_time']}")
            print(f"執行時間: {info['execution_time']}")
        
        print("\n【研究結果】")
        for i, research in enumerate(final_state['research_results'], 1):
            print(f"\n研究 {i}:")
            print(research)
        
        print("\n【分析結果】")
        for i, analysis in enumerate(final_state['analysis_results'], 1):
            print(f"\n分析 {i}:")
            print(analysis)
            
    except Exception as e:
        print(f"\n工作流執行出錯: {str(e)}")
        logger.error(f"工作流執行錯誤: {str(e)}", exc_info=True)
        return
>>>>>>> Stashed changes

if __name__ == "__main__":
    main() 