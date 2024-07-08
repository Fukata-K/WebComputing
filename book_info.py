import streamlit as st
import requests


# book_infoを受け取り表示する関数
def display_book_info(book_info):

    st.write('タイトル: ', book_info['タイトル'])

    try: st.image(book_info["画像"], '本の画像')
    except Exception as _: pass

    try: st.write('著者　　: ', ' ・ '.join(book_info['著者']))
    except KeyError as _: pass

    try: st.write('出版社　: ', book_info['出版社'])
    except KeyError as _: pass

    try: st.write('出版日　: ', book_info['出版日'])
    except KeyError as _: pass

    try: st.write('ページ数: ', str(book_info['ページ数']))
    except KeyError as _: pass

    try: st.write('推薦理由: ', book_info['推薦理由'])
    except KeyError as _: pass

    try: st.write('要約　　: ', book_info['要約'])
    except KeyError as _: pass

    try: st.write('カテゴリ: ', ' ・ '.join(book_info['カテゴリ']))
    except KeyError as _: pass

    try: st.write('Googleブックスのリンク　: ', book_info['本のリンク'])
    except KeyError as _: pass

    st.write('\n')
    st.write('\n')


# books_listを受け取り順に表示する関数
def display_books_list(books_list):

    for i, book in enumerate(books_list):
        st.subheader(f"{i+1}冊目")
        display_book_info(book)