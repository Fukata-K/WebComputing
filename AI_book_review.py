import streamlit as st
import openai

# GPTのAPIキーを設定
openai.api_key = st.secrets['GPT_API_KEY']


# 受け取った本の情報をもとにChatGPTから書評を受け取る関数
def book_review_GPT(book_info):

    # 本を書評するように設定する
    gpt_role = "あなたは本の書評を行うAIです．受け取った本の情報とあなた自身の知識を利用して書評を書きます．"

    # プロンプトを作成
    prompt = "以下の書誌情報をもとに書評を書いてください．\n\n"
    prompt += "-----------------------------------------\n"

    try: prompt += f"タイトル: 『{book_info['タイトル']}』\n"
    except KeyError as _: pass

    try: prompt += f"著者: {book_info['著者']}\n"
    except KeyError as _: pass

    try: prompt += f"出版社: {book_info['出版社']}\n"
    except KeyError as _: pass

    try: prompt += f"出版日: {book_info['出版日']}\n"
    except KeyError as _: pass

    try: prompt += f"ページ数: {str(book_info['ページ数'])}\n"
    except KeyError as _: pass

    try: prompt += f"本の要約: {str(book_info['要約'])}\n"
    except KeyError as _: pass

    try: prompt += f"カテゴリ: {' ・ '.join(book_info['カテゴリ'])}\n"
    except KeyError as _: pass

    prompt += "-----------------------------------------\n"

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": gpt_role},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content
