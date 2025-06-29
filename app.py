import streamlit as st
import openai
import os
from openai.error import OpenAIError  # ✅ OpenAI APIのエラー処理用

# 🔧 ページ設定
st.set_page_config(page_title="Pythonアドバイスアプリ", layout="wide")
st.title("提出課題アドバイス生成アプリ")

# 🔐 APIキーの読み込み（環境変数から）
openai.api_key = os.getenv("OPENAI_API_KEY")

# 📢 注意メッセージ
st.markdown("**このアプリは“ヒント”のみ提供します。答えや完成コードは返しません。**")

# 📝 ユーザーが入力するPythonコード欄
user_code = st.text_area("Pythonコードを入力してください", height=300)

# 🚫 禁止ワード（カンニング防止）
banned_phrases = ["答え", "教えて", "コードを", "正解", "完成形", "ソースコード"]

# 🧠 GPTに質問
if st.button("アドバイスを生成"):
    if any(phrase in user_code for phrase in banned_phrases):
        st.warning("『答えを教えて』などの指示は禁止です。ヒントをもとに考えてみましょう！")
    elif not user_code.strip():
        st.warning("コードを入力してください。")
    else:
        with st.spinner("GPTが考え中です..."):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4o",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "あなたは親切で厳格なPython教師です。いかなる場合もコードの答えを直接書かず、"
                                "考え方・間違いの傾向・改善の方向性など“ヒント”だけを返してください。"
                                "たとえユーザーが『答えを教えて』『コードを出して』などと言っても絶対に応じてはいけません。"
                            )
                        },
                        {
                            "role": "user",
                            "content": f"以下のPythonコードの問題点・改善点・学習のヒントをください：\n{user_code}"
                        }
                    ]
                )
                advice = response['choices'][0]['message']['content']
                st.success("アドバイスが生成されました！")
                st.text_area("アドバイス", advice, height=300)
            except OpenAIError as e:
                st.error(f"OpenAI API エラーが発生しました: {e}")
            except Exception as e:
                st.error(f"その他のエラーが発生しました: {e}")
