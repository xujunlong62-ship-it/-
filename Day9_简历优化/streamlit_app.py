import streamlit as st
import pdfplumber
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import ai, optimize_resume, generate_interview_questions, score_match

st.set_page_config(page_title="简历优化助手", page_icon="📄", layout="wide")

st.title("📄 简历优化助手")
st.markdown("上传你的简历 PDF + 粘贴职位描述(JD)，一键生成优化版简历、面试题库和匹配评分")

# Sidebar
with st.sidebar:
    st.header("⚙️ 设置")
    api_key = st.text_input("API Key（可选，默认使用.env配置）", type="password")
    if api_key:
        os.environ["dashscope_api_key"] = api_key

# Main area
col1, col2 = st.columns(2)

with col1:
    st.subheader("📎 上传简历")
    uploaded_file = st.file_uploader("选择简历 PDF 文件", type=["pdf"])
    
    if uploaded_file is not None:
        with st.spinner("正在解析 PDF..."):
            try:
                with pdfplumber.open(uploaded_file) as pdf:
                    resume_text = ""
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            resume_text += page_text + "\n"

                st.success(f"✅ 成功解析 PDF（{len(resume_text)} 字符）")
                with st.expander("查看提取的文本"):
                    st.text(resume_text)
            except Exception as e:
                st.error(f"❌ 解析失败：{e}")
                resume_text = ""

with col2:
    st.subheader("📝 职位描述 (JD)")
    jd_text = st.text_area("粘贴职位描述", height=300, placeholder="请粘贴你要应聘的职位描述...")
    
    tab1, tab2, tab3 = st.columns(3)
    
    with tab1:
        btn_optimize = st.button("🚀 优化简历", use_container_width=True)
    with tab2:
        btn_questions = st.button("❓ 生成面试题", use_container_width=True)
    with tab3:
        btn_score = st.button("📊 匹配评分", use_container_width=True)

# Results area
if not resume_text:
    st.info("👆 请先上传简历 PDF 文件")
elif not jd_text:
    st.warning("⚠️ 请粘贴职位描述 (JD)")

if btn_optimize and resume_text and jd_text:
    with st.spinner("🔄 AI 正在优化简历..."):
        optimized = optimize_resume(resume_text, jd_text)
    st.subheader("✅ 优化后的简历")
    st.markdown("---")
    st.markdown(optimized)
    
    # Download button
    st.download_button(
        label="📥 下载优化版简历",
        data=optimized,
        file_name="optimized_resume.txt",
        mime="text/plain"
    )

if btn_questions and resume_text and jd_text:
    with st.spinner("🔄 AI 正在生成面试题..."):
        questions = generate_interview_questions(resume_text, jd_text)
    st.subheader("❓ 面试题库")
    st.markdown("---")
    st.markdown(questions)
    
    st.download_button(
        label="📥 下载面试题库",
        data=questions,
        file_name="interview_questions.txt",
        mime="text/plain"
    )

if btn_score and resume_text and jd_text:
    with st.spinner("🔄 AI 正在评估匹配度..."):
        score = score_match(resume_text, jd_text)
    
    st.subheader("📊 匹配评分")
    st.markdown("---")
    
    # Score display with color
    score_color = "green" if score >= 80 else "orange" if score >= 60 else "red"
    st.markdown(f"<h1 style='color: {score_color}; text-align: center;'>{score}/100</h1>", unsafe_allow_html=True)
    
    if score >= 80:
        st.success("🎉 匹配度很高！你的背景非常符合这个职位。")
    elif score >= 60:
        st.warning("💪 匹配度中等，简历优化后可以进一步提升。")
    else:
        st.error("📈 匹配度较低，建议针对JD重点优化简历内容。")

# Footer
st.markdown("---")
st.caption("Powered by Dashscope Qwen + Streamlit")
