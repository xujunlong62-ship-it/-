# Day 9-10: 简历优化助手

AI 驱动的简历优化工具，支持 CLI 和 Web 界面。

## 功能

- CLI 模式：交互式输入 / 演示模式生成 Word 简历 + 面试题库
- Web 界面：上传 PDF + 粘贴 JD → 实时生成优化版简历、面试题、匹配评分
- 部署就绪：一键部署到 Streamlit Cloud (share.streamlit.io)

## 快速开始

### 1. 安装依赖
`powershell
cd D:\\学习总结\\Day9_简历优化
.venv\\Scripts\\activate
pip install -r requirements.txt
`

### 2. 配置 API Key
`powershell
copy .env.example .env
# 编辑 .env 填入 dashscope_api_key
`

## 部署到 Streamlit Cloud

1. 推送代码到 GitHub
`powershell
git init
git add .
git commit -m "Day 9-10: Resume optimizer with Streamlit"
git remote add origin https://github.com/USERNAME/Day9_简历优化.git
git push -u origin main
`
2. 关联 Streamlit Cloud
   - 打开 https://share.streamlit.io
   - 点击 **New app** → 选择 GitHub 仓库
   - Main file path: streamlit_app.py
   - 点击 **Deploy**

3. 配置 Secret
   - 部署成功后，点击应用右上角 **⋮ → Settings → Secrets**
   - 添加：
   `	oml
   DASHSCOPE_API_KEY = "sk-xxxxxxxxxxxx"
   `
   - 保存 → 应用自动重启

## 项目结构

`
Day9_简历优化/
├── main.py                 # 核心逻辑 + CLI
├── streamlit_app.py        # Streamlit Web 界面
├── requirements.txt        # 依赖列表
├── .env.example            # 环境变量模板
├── .env                    # 本地环境变量（不提交）
├── .gitignore
├── .streamlit/
│   └── config.toml         # Streamlit 配置
├── README.md
└── .venv/                  # 虚拟环境
`
## 核心函数（供 Web 调用）

`python
from main import optimize_resume, generate_interview_questions, score_match

optimized = optimize_resume(resume_text, jd_text)        # 返回 Markdown
questions = generate_interview_questions(resume_text, jd_text)  # 返回 Markdown
score = score_match(resume_text, jd_text)                # 返回 0-100
`

## 环境变量

| 变量 | 说明 |
|------|------|
| dashscope_api_key | 阿里云百炼 API Key |
| dashscope_base_url | 可选，默认 https://dashscope.aliyuncs.com/compatible-mode/v1 |

## 许可证

MIT