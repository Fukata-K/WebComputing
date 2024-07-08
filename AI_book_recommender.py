import streamlit as st
import openai
import re
from google_books import search_book, make_books_list

# GPTのAPIキーを設定
openai.api_key = st.secrets['GPT_API_KEY']


# 受け取ったプロンプトをもとにChatGPTから推薦図書を受け取る関数
def book_recommender_GPT(prompt):

    gpt_role = 'あなたは本の推薦を行うAIです．受け取ったテキストから情報からあなた自身の知識を利用して本をお勧めします．'

    response = openai.chat.completions.create(
        # model='gpt-4o',
        model='gpt-3.5-turbo',  # modelを変えるときはここを変更
        messages=[
            {'role': 'system', 'content': gpt_role},
            {'role': 'user', 'content': prompt}
        ]
    )

    answer = response.choices[0].message.content

    return answer


# 読みたい本のテキストでの説明と冊数を受け取り推薦図書を返す関数
def book_recommend_text(text, num_recommend_books):

    prompt = 'あなたは選書を行うAIです．以下のような依頼に対して適切な本を推薦してください．\n\n'
    prompt += '------------------------------------------------\n'
    prompt += text
    prompt += '------------------------------------------------\n\n'
    prompt += '必ず以下の形式に順守して回答してください．\n'
    prompt += '推薦理由は3行程度で書いてください．\n'
    prompt += f'必ず{num_recommend_books}冊の本を紹介してください．\n'
    prompt += '------------------------------------------------\n'
    for i in range(num_recommend_books):
        prompt += f'{i+1}冊目：『{i+1}冊目の本のタイトル』({i+1}冊目の本の著者)'
        prompt += '推薦理由：ここに推薦理由を3行程度で書いてください'
    prompt += '------------------------------------------------\n\n'
    
    return book_recommender_GPT(prompt)


# 本のリストと冊数を受け取り推薦図書を返す関数 (fav_books[i] = ['タイトル', '著者'])
def book_recommend_list(fav_books, num_recommend_books):
    
    prompt = 'あなたは選書を行うAIです．以下の本を読んだ人に対して次に読むのに適切な本を推薦してください．\n\n'
    prompt += '------------------------------------------------\n'
    for title, author in fav_books:
        prompt += f'『{title}』({author})'
    prompt += '------------------------------------------------\n\n'
    prompt += '必ず以下の形式に順守して回答してください．\n'
    prompt += '推薦理由は3行程度で書いてください．\n'
    prompt += f'必ず{num_recommend_books}冊の本を紹介してください．\n'
    prompt += '------------------------------------------------\n'
    for i in range(num_recommend_books):
        prompt += f'{i+1}冊目：『{i+1}冊目の本のタイトル』({i+1}冊目の本の著者)'
        prompt += '推薦理由：ここに推薦理由を3行程度で書いてください'
    prompt += '------------------------------------------------\n\n'
    
    return book_recommender_GPT(prompt)


# GPTからの本の推薦を受け取り整形して返す関数
def recommended_text_to_books_list(recommended_text):
    # 本のタイトルと著者の抽出パターン
    book_pattern = re.compile(r'『(.+?)』\((.+?)\)')

    # 推薦理由の抽出パターン
    reason_pattern = re.compile(r'推薦理由：(.+?)(?=\n\d冊目|$)', re.DOTALL)

    # 本のリストと推薦理由のリストを初期化
    recommended_books_list = []
    recommend_reasons_list = []

    # 本の情報の抽出
    book_matches = book_pattern.findall(recommended_text)
    for title, author in book_matches:
        recommended_books_list.append(f'{title} {author}')

    # 推薦理由の抽出
    reason_matches = reason_pattern.findall(recommended_text)
    for reason in reason_matches:
        recommend_reasons_list.append(reason.strip())


    try:
        book_info_list = []
        for book in recommended_books_list:
            book_info_list.append(search_book(book)[0])
        books_list = make_books_list(book_info_list)

    except Exception as _:
        books_list = []
        for i, book in enumerate(recommended_books_list):
            book = {}
            title, author = book_matches[i]
            book['タイトル'] = title
            book['著者'] = [author]
            st.write(book_matches[i])
            st.write(book)
            books_list.append(book)

    # 本の情報に推薦理由を加える
    for i, book in enumerate(books_list):
        book['推薦理由'] = recommend_reasons_list[i]
        
    return books_list


# テキストで検索時に実行する関数
def search_text(text, num_recommend_books):
    recommended_text = book_recommend_text(text, num_recommend_books)
    books_list = recommended_text_to_books_list(recommended_text)
    
    return books_list


# 本のリストから検索する時に実行する関数
def search_fav_books_list(fav_books, num_recommend_books):
    recommended_text = book_recommend_list(fav_books, num_recommend_books)
    books_list = recommended_text_to_books_list(recommended_text)
    
    return books_list