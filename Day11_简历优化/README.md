# Day 9: AI Agent 协作简历优化流水线

## 简介

3 个 AI 角色接力工作，自动优化你的简历并生成面试问题：

1. **分析师** — 读取简历 + JD，打分（100 分制），找出差距
2. **优化师** — 根据分析结果优化简历（低分重写，高分微调）
3. **教练** — 根据优化简历生成 8 个高频面试问题

## 条件分支

- 如果分析师打分低于 60 分，优化师会**彻底重写**简历；
- 如果 60 分以上，只做**微调优化**。

## 快速开始

`powershell
cd Day9_简历优化
uv venv
uv pip install -r requirements.txt
copy .env.example .env
uv run python main.py
`

## 环境配置

1. 前往 [阿里云百炼平台](https://bailian.console.aliyun.com/) 获取 API Key
2. 将 .env.example 复制为 .env
3. 将你的 API Key 填入 .env 文件中

`
dashscope_api_key=sk-你的实际API_KEY
dashscope_base_url=https://dashscope.aliyuncs.com/compatible-mode/v1
`

## 工作流程

运行后按提示依次输入：
- 基本信息（姓名、电话、邮箱、目标职位、学校、专业等）
- 工作经历（每段经历单独描述，输入"结束"完成）
- 项目经历（每个项目单独描述，输入"结束"完成）

## 依赖

- [langgraph](https://github.com/langchain-ai/langgraph) 1.2.9 — AI Agent 框架
- [openai](https://github.com/openai/openai-python) 2.49.0 — OpenAI 兼容 API 客户端
- [python-dotenv](https://github.com/theskumar/python-dotenv) 1.2.2 — 环境变量加载
- [python-docx](https://github.com/python-openxml/python-docx) 1.2.0 — Word 文档生成

## License

MIT
