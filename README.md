# Multi-Agent System with LangGraph

這是一個基於 LangGraph 的多智能體系統，用於協同完成複雜任務。系統包含三個專門的智能體：
1. 研究員 (Researcher)：負責收集和分析信息
2. 分析師 (Analyst)：負責處理和總結信息
3. 決策者 (Decision Maker)：負責做出最終決策

## 功能特點

- 基於 LangGraph 的工作流程管理
- 多個專門的智能體協同工作
- 清晰的任務分解和執行流程
- 可擴展的架構設計

## 安裝

1. 克隆此倉庫
2. 安裝依賴：
```bash
pip install -r requirements.txt
```

## 配置

1. 創建 `.env` 文件並設置 OpenAI API Key：
```bash
# .env
OPENAI_API_KEY=your-api-key-here
```

## 使用方法

1. 修改 `main.py` 中的任務描述
2. 運行程序：
```bash
python main.py
```

## 系統架構

- `agents.py`: 包含所有智能體的定義
- `main.py`: 主程序和工作流程定義
- `.env`: 環境變量配置文件

## 工作流程

1. 研究員接收任務並進行初步研究
2. 分析師處理研究結果並提供分析
3. 決策者根據分析做出最終決策

## 自定義

你可以通過以下方式自定義系統：

1. 在 `agents.py` 中添加新的智能體
2. 修改現有智能體的提示詞
3. 在 `main.py` 中調整工作流程

## 注意事項

- 確保有足夠的 OpenAI API 額度
- 根據需要調整智能體的溫度參數
- 可以根據具體任務調整提示詞
- 請確保 `.env` 文件已經正確配置 