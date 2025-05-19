
import streamlit as st
import json
import pandas as pd

st.set_page_config(page_title="Texas Irrigator License - Practice Exam (All Questions)", layout="wide")
st.title("📚 Texas Irrigator License - Practice Exam (All Questions)")
st.markdown("请依次作答以下所有题目，答错将记录到错题集。")

try:
    with open('irrigation_exam_questions_classified_bilingual.json', 'r', encoding='utf-8') as f:
        questions = json.load(f)
except FileNotFoundError:
    st.error("⚠️ 未找到 irrigation_exam_questions_classified_bilingual.json 文件，请与本程序放在同一目录下。")
    st.stop()

if 'wrong_answers' not in st.session_state:
    st.session_state.wrong_answers = []

score = 0
answers = {}

for i, q in enumerate(questions):
    st.markdown(f"### Q{i+1}: {q['question_en']}\n#### 🈶 中文：{q['question_zh']}")
    user_answer = st.radio("请选择一个答案：", q['options'], key=f"q{i}")
    answers[f"q{i}"] = user_answer

if all(answers[f"q{i}"] is not None for i in range(len(questions))) and st.button("📋 提交并查看得分"):
    for i, q in enumerate(questions):
        user_answer = answers[f"q{i}"]
        if user_answer == q['answer']:
            st.success(f"Q{i+1} ✅ 正确")
            score += 1
        else:
            st.error(f"Q{i+1} ❌ 错误，正确答案是：{q['answer']}")
            st.info(f"📘 解释：{q.get('explanation', '无解释提供')}")
            st.session_state.wrong_answers.append({
                "question_en": q["question_en"], "question_zh": q["question_zh"],
                "your_answer": user_answer,
                "correct_answer": q["answer"],
                "explanation": q.get("explanation", "")
            })

    st.markdown("---")
    st.subheader(f"🎯 最终得分：{score} / {len(questions)}")

    if score >= int(len(questions) * 0.95):
        st.success("🎉 恭喜你通过了模拟考试！")
    else:
        st.warning("📘 请继续努力，目标是至少答对 95%。")

    if st.session_state.wrong_answers:
        df = pd.DataFrame(st.session_state.wrong_answers)
        st.download_button(
            label="📥 下载错题记录",
            data=df.to_csv(index=False),
            file_name="irrigation_wrong_answers.csv",
            mime="text/csv"
        )
