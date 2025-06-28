import streamlit as st
import openai
import os

# Streamlitの設定
st.set_page_config(page_title="Pythonアドバイスアプリ", layout="wide")
st.title("提出課題アドバイス生成アプリ")

# OpenAIクライアント初期化（v1以降の形式）
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ユーザーの入力欄
user_code = st.text_area("Pythonコードを入力してください", height=300)

if st.button("アドバイスを生成"):
    with st.spinner("GPTが考え中です..."):
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "あなたはPython教師です。答えを直接教えずにヒントを出してください。"},
                    {"role": "user", "content": f"以下のコードの問題点と改善点、学習のヒントをください:\n{user_code}"}
                ]
            )
            advice = response.choices[0].message.content
            st.success("アドバイスが生成されました！")
            st.text_area("アドバイス", advice, height=300)
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")
