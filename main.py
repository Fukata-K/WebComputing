import streamlit as st
from google_books import search_books_keyword
from book_info import display_books_list
from more_info import more_books_info
from AI_book_recommender import search_text, search_fav_books_list

# 以下のコマンドでローカル環境で実行
# streamlit run main.py


# 0.タイトル及び説明文
st.title('本検索/選書AIサービス')
st.header('0. 使い方')
st.write('様々な入力形式からAIが選書を行うサービスです')


# 1.セレクトボックスで検索方式を決定する
st.header('1. 検索する方法を決めてください')
st.write('①キーワード検索 (例: プログラミング)')
st.write('②文章で検索 (例: 衝撃的な推理小説が読みたいです)')
st.write('③本のリストで検索')
how_to_search = st.selectbox('検索方法', ['キーワード', '文章で検索', '本のリスト'])


# 2.検索方式に合わせて入力を受け取る
if how_to_search == 'キーワード': st.header('2. 検索キーワードを入力してください')
if how_to_search == '文章で検索': st.header('2. 検索する文章を入力してください')
if how_to_search == '本のリスト': st.header('2. 好きな本を入力してください')

with st.form(key='recommend_form'):
    if how_to_search == 'キーワード':
        keyword = st.text_input('検索するキーワード')

    if how_to_search == '文章で検索':
        text = st.text_input('検索する文章')

    if how_to_search == '本のリスト':
        fav_books = []

        for i in range(5):
            fav_book = st.text_input(f'{i+1}冊目のタイトル')
            fav_book_author = st.text_input(f'{i+1}冊目の著者 (省略可)')

            if fav_book != '':
                fav_books.append([fav_book, fav_book_author])

    # スライダーで出力する本の冊数を決める
    num_recommend_books = st.slider(f'紹介して欲しい本の冊数を決めてください (最大で5冊)', 1, 5, 3)

    # 送信ボタン
    submit_btn = st.form_submit_button('送信')


# 2.5.検索方式に合わせて本を探す
if submit_btn:

    # 本の情報を保持するリスト
    books_list = []

    # キーワード検索
    if how_to_search == 'キーワード':
        if keyword == '':
            st.write('キーワードを入力してください')
        else:
            try: books_list = search_books_keyword(keyword, num_recommend_books)
            except Exception as _: 
                st.write('大変申し訳ございませんが現在キーワード検索はご利用いただけません')
                st.write('他の検索方法をお試しください')

    # 文章で検索
    if how_to_search == '文章で検索':
        if text == '':
            st.write('文章を入力してください')
        else:
            try: books_list = search_text(text, num_recommend_books)
            except Exception as _:
                st.write('読み込みに失敗しました')
                st.write('再度テキストを入力し直してください')

    # 本のリストで検索
    if how_to_search == '本のリスト':
        if fav_books == []:
            st.write('最低でも1冊はタイトルを入力してください')
        else:
            st.write('あなたの入力内容')
            for i, book in enumerate(fav_books):
                if book[1] != '':
                    st.write(f'{i+1}冊目:『{book[0]}』({book[1]})')
                else:
                    st.write(f'{i+1}冊目:『{book[0]}』')
            
            try: books_list = search_fav_books_list(fav_books, num_recommend_books)
            except Exception as _: 
                st.write('読み込みに失敗しました')
                st.write('再度リストを入力し直してください')


# 3.検索結果を表示する
if submit_btn and len(books_list):
    st.header('3. 検索結果の一覧')
    display_books_list(books_list)


# 4.表示された本の中から気になる本の詳細を表示する
if submit_btn and len(books_list):
    st.header('4. さらに本に関する情報を見る')
    st.write('ここでは検索結果の本に関して以下の情報を得ることができます')
    st.write('① 楽天市場での検索結果 (あれば)')
    st.write('② YouTubeでの検索結果 (あれば)')
    st.write('③ AIによる書評')
    st.write('注: 簡易的な検索なので関係のないものが表示されることがあります')
    
    for i, book in enumerate(books_list):
        st.subheader(f'{i+1}冊目:『{book["タイトル"]}』の詳細')
        more_books_info(books_list[i])