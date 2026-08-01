import streamlit as st
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import (
    ai,
    build_resume_text,
    get_demo_info,
    generate_resume,
    polish_resume,
    generate_interview_questions,
    optimize_resume,
    score_match,
    save_word,
    save_questions,
)

st.set_page_config(page_title="简历生成与优化助手", page_icon="\U0001f4c4", layout="wide")
st.title("\U0001f4c4 简历生成与优化助手")

# ========== 选择模式 ==========
mode = st.radio(
    "选择功能模式：",
    ["\u270f\ufe0f 一键生成简历", "\U0001f4ce 上传PDF优化简历", "\U0001f3ad 示例演示（一键出样）"],
    horizontal=True,
)


def generate_word_download(resume_text, filename="简历.docx"):
    import tempfile, os
    tmp_path = os.path.join(tempfile.gettempdir(), f"resume_{abs(hash(filename))}.docx")
    if os.path.exists(tmp_path):
        os.unlink(tmp_path)
    try:
        save_word(resume_text, tmp_path)
        with open(tmp_path, "rb") as f:
            return f.read()
    finally:
        try:
            os.unlink(tmp_path)
        except:
            pass


def show_resume_preview(resume_text, docx_bytes, name="简历"):
    st.success(f"\u2705 {name}生成完成！")
    st.markdown("---")
    st.markdown("### \U0001f4dd 简历预览")
    st.markdown(resume_text)
    st.markdown("---")
    st.download_button(
        label="\U0001f4e5 下载 Word 文档",
        data=docx_bytes,
        file_name=f"{name}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        use_container_width=True,
    )


# ========== 模式1：一键生成 ==========
if mode == "\u270f\ufe0f 一键生成简历":
    st.subheader("\u270f\ufe0f 填写信息，一键生成简历")

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("姓名")
        phone = st.text_input("电话")
        email = st.text_input("邮箱")
        position = st.text_input("目标职位")
        school = st.text_input("学校")
    with col2:
        major = st.text_input("专业")
        degree = st.selectbox("学历", ["", "大专", "本科", "硕士", "博士"])
        grad_year = st.text_input("毕业时间")
        skills = st.text_area("技能（逗号分隔）", placeholder="Python, Java, SQL")

    st.markdown("#### 工作经历")
    work_count = st.number_input("工作经历段数", min_value=0, max_value=5, value=1)
    work_exps = []
    for i in range(int(work_count)):
        exp = st.text_area(f"工作经历 {i+1}", key=f"work_{i}", height=80)
        if exp:
            work_exps.append(exp)

    st.markdown("#### 项目经历")
    proj_count = st.number_input("项目经历段数", min_value=0, max_value=5, value=1)
    projects = []
    for i in range(int(proj_count)):
        proj = st.text_area(f"项目经历 {i+1}", key=f"proj_{i}", height=80)
        if proj:
            projects.append(proj)

    jd_generate = st.text_area("职位描述（选填，用于针对性优化）", height=100)

    if st.button("\U0001f680 生成简历", type="primary", use_container_width=True):
        if not name:
            st.error("请至少输入姓名")
        else:
            info = {
                "name": name,
                "phone": phone,
                "email": email,
                "position": position,
                "school": school,
                "major": major,
                "degree": degree,
                "grad_year": grad_year,
                "skills": skills,
                "work_exps": work_exps,
                "projects": projects,
            }
            with st.status("\U0001f504 正在生成简历...", expanded=True) as status:
                st.write("AI 正在根据填写信息生成简历...")
                resume_raw = generate_resume(info)
                resume_text = polish_resume(resume_raw) if not jd_generate else resume_raw

                if jd_generate:
                    st.write("正在根据职位描述优化简历...")
                    resume_text = optimize_resume(resume_text, jd_generate)

                st.write("正在生成 Word 文档...")
                docx_bytes = generate_word_download(resume_text, f"{name}_简历.docx")
                status.update(label="\u2705 简历生成完成！", state="complete")

            show_resume_preview(resume_text, docx_bytes, name)

            with st.spinner("\U0001f504 正在生成面试题库..."):
                questions = generate_interview_questions(resume_text, jd_generate or None)
            with st.expander("\u2753 查看面试题库"):
                st.markdown(questions)

# ========== 模式2：上传PDF优化 ==========
elif mode == "\U0001f4ce 上传PDF优化简历":
    st.subheader("\U0001f4ce 上传简历 PDF + 职位描述 → 优化")

    col1, col2 = st.columns(2)
    with col1:
        uploaded_file = st.file_uploader("选择简历 PDF", type=["pdf"])
        resume_text = ""
        if uploaded_file:
            try:
                import pdfplumber
                with pdfplumber.open(uploaded_file) as pdf:
                    for page in pdf.pages:
                        pt = page.extract_text()
                        if pt:
                            resume_text += pt + "\n"
                st.success(f"\u2705 已解析 PDF（{len(resume_text)} 字符）")
                with st.expander("查看提取的文本"):
                    st.text(resume_text)
            except Exception as e:
                st.error(f"解析失败：{e}")

    with col2:
        jd_text = st.text_area("职位描述 (JD)", height=200)

    if resume_text and jd_text:
        c1, c2, c3 = st.columns(3)
        with c1:
            btn_optimize = st.button("\U0001f680 优化简历", use_container_width=True, type="primary")
        with c2:
            btn_questions = st.button("\u2753 面试题", use_container_width=True)
        with c3:
            btn_score = st.button("\U0001f4ca 匹配评分", use_container_width=True)

        if btn_optimize:
            with st.spinner("\U0001f504 AI 正在优化..."):
                optimized = optimize_resume(resume_text, jd_text)
            st.markdown("---")
            st.markdown("### \u2705 优化后的简历（预览）")
            st.markdown(optimized)
            st.download_button(
                "\U0001f4e5 下载优化版", optimized,
                file_name="optimized_resume.txt",
                use_container_width=True,
            )

        if btn_questions:
            with st.spinner("\U0001f504 AI 正在生成面试题..."):
                questions = generate_interview_questions(resume_text, jd_text)
            st.markdown("---")
            st.markdown("### \u2753 面试题库")
            st.markdown(questions)
            st.download_button(
                "\U0001f4e5 下载面试题库", questions,
                file_name="interview_questions.txt",
                use_container_width=True,
            )

        if btn_score:
            with st.spinner("\U0001f504 AI 正在评估..."):
                score = score_match(resume_text, jd_text)
            color = "green" if score >= 80 else "orange" if score >= 60 else "red"
            st.markdown(f"<h1 style='color:{color};text-align:center;'>{score}/100</h1>", unsafe_allow_html=True)

    elif not resume_text and uploaded_file is not None:
        st.warning("\u26a0\ufe0f 请填写职位描述")
    elif not resume_text:
        st.info("\U0001f446 请先上传 PDF 简历")

# ========== 模式3：示例演示 ==========
elif mode == "\U0001f3ad 示例演示（一键出样）":
    st.subheader("\U0001f3ad 示例演示 — 无需填写，一键出样")
    st.info("点击下方按钮，AI 会自动使用内置示例数据生成一份完整的简历（含 Word 下载和面试题库）")

    if st.button("\U0001f680 一键生成示例简历", type="primary", use_container_width=True):
        with st.status("\U0001f504 正在生成示例简历...", expanded=True) as status:
            st.write("加载示例数据...")
            info = get_demo_info()

            st.write("AI 正在生成简历...")
            resume_raw = generate_resume(info)

            st.write("AI 正在润色优化...")
            resume_text = polish_resume(resume_raw)

            st.write("正在生成 Word 文档...")
            docx_bytes = generate_word_download(resume_text, "示例简历.docx")

            status.update(label="\u2705 示例简历生成完成！", state="complete")

        show_resume_preview(resume_text, docx_bytes, "示例简历")

        with st.spinner("\U0001f504 正在生成面试题库..."):
            questions = generate_interview_questions(resume_text)
        with st.expander("\u2753 查看面试题库"):
            st.markdown(questions)

st.markdown("---")
st.caption("Powered by Dashscope Qwen + Streamlit");
