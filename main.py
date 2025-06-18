from typing import Dict, List, Any, TypedDict
import logging
from dotenv import load_dotenv
import time
from datetime import datetime
import json
import os
from workflow import create_workflow, create_initial_state

# 加載環境變量
load_dotenv()

# 檢查 API key
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("請在 .env 文件中設置 OPENAI_API_KEY 環境變量")

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
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
    
    # 創建工作流
    workflow = create_workflow()
    
    # 創建初始狀態
    initial_state = create_initial_state(task)
    
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

if __name__ == "__main__":
    main() 