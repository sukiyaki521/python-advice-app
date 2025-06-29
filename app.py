import streamlit as st
import openai
import os

st.set_page_config(page_title="Pythonアドバイスアプリ", layout="wide")
st.title("提出課題アドバイス生成アプリ")

openai.api_key = os.getenv("OPENAI_API_KEY")

st.markdown("**このアプリは“ヒント”のみ提供します。答えや完成コードは返しません。**")

user_code = st.text_area("Pythonコードを入力してください", height=300)

banned_phrases = ["答え", "教えて", "コードを", "正解", "完成形", "ソースコード"]

if st.button("アドバイスを生成"):
    if any(phrase in user_code for phrase in banned_phrases):
        st.warning("『答えを教えて』などの指示は禁止です。ヒントをもとに考えてみましょう！")
    elif not user_code.strip():
        st.warning("コードを入力してください。")
    else:
        with st.spinner("GPTが考え中です..."):
            try:
                response = openai.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "あなたは親切で厳格なPython教師です。コードの答えは書かず、"
                                "考え方・間違いの傾向・改善の方向性など“ヒント”のみを返してください。"
                            )
                        },
                        {
                            "role": "user",
                            "content": f"以下のPythonコードの問題点・改善点・学習のヒントをください：\n{user_code}"
                        }
                    ]
                )
                advice = response.choices[0].message.content
                st.success("アドバイスが生成されました！")
                st.text_area("アドバイス", advice, height=300)
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
