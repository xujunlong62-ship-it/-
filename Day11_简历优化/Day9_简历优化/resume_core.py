# 核心简历优化函数
from main import ai

def optimize_resume(resume_text, jd_text):
    prompt = f"""你是资深简历优化专家。根据职位描述(JD)优化简历，使简历更匹配该职位。

职位描述：
{jd_text}

原始简历：
{resume_text}

请输出优化后的完整简历，保持原有格式。
"""
    return ai(prompt)


def generate_interview_questions(resume_text, jd_text):
    prompt = f"""你是资深面试官。根据简历和职位描述生成8个高频面试问题。

简历：
{resume_text}

职位要求：
{jd_text}

输出格式：每个问题前加[Q:]前缀。
"""
    return ai(prompt)


def score_match(resume_text, jd_text):
    prompt = f"""你是招聘系统匹配算法。分析以下简历与职位描述(JD)的匹配程度，只输出0-100的数字。

简历：
{resume_text}

职位描述：
{jd_text}

匹配分数（只输出数字）："""
    try:
        result = ai(prompt).strip()
        return int(result)
    except:
        return 60
