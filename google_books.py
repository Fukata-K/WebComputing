import streamlit as st
import requests

GOOGLE_BOOKS_API_KEY = st.secrets['GOOGLE_API_KEY']


# 文字列keywordを受け取りGoogleブックスでの検索結果をリストとして返す関数
def search_book(keyword):

    url = "https://www.googleapis.com/books/v1/volumes"
    params = {"q": keyword, "maxResults": 7, "key": GOOGLE_BOOKS_API_KEY}
    response = requests.get(url, params=params).json() #情報の取得,json変換
    items_list = response['items'] #items リストデータ

    return items_list


# 1つのitem情報を受け取り整形した辞書として返す関数
def make_book_info(item):
    book_info = {}
    item = item['volumeInfo']

    book_info['タイトル'] = item['title']

    try: book_info['画像'] =     item['imageLinks']['thumbnail']
    except KeyError as _: pass

    try: book_info['著者'] =     item['authors']
    except KeyError as _: pass

    try: book_info['出版社'] =   item['publisher']
    except KeyError as _: pass

    try: book_info['出版日'] =   item['publishedDate']
    except KeyError as _: pass

    try: book_info['ページ数'] = item['pageCount']
    except KeyError as _: pass

    try: book_info['要約'] =     item['description']
    except KeyError as _: pass

    try: book_info['カテゴリ'] = item['categories']
    except KeyError as _: pass

    try: book_info['本のリンク']=item['previewLink']
    except KeyError as _: pass

    return book_info


# 検索結果のリストから整形した辞書のリストを返す関数
def make_books_list(items_list):
    books_list = []

    for item in items_list:
        books_list.append(make_book_info(item))

    return books_list


# キーワードから本を検索し指定した個数分の情報を含むリストを返す関数
def search_books_keyword(keyword, books_num):

    items_list = search_book(keyword)

    return make_books_list(items_list[:books_num])