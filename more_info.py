import streamlit as st

from AI_book_review import book_review_GPT
from rakuten_search import search_rakuten, display_rakuten_info
from youtube_search import search_youtube, display_youtube_info


# book_infoを受け取り, 楽天/Youtubeのリンク, AIによる書評を表示する
def more_books_info(book_info):
    
    search_word = book_info['タイトル']
    
    try: search_word += ' ' + ' '.join(book_info['著者'])
    except Exception as _: pass
    
    # 楽天の情報を表示する部分
    try:
        rakuten_item_info = search_rakuten(search_word)
        display_rakuten_info(rakuten_item_info)
    except Exception as _: pass
    
    # YouTubeの情報を表示する部分
    try:
        youtube_items = search_youtube(search_word)
        for youtube_info in youtube_items:
            display_youtube_info(youtube_info, book_info['タイトル'])
    except Exception as _: pass
    
    # AI(Chat GPT)による書評を表示する部分
    try:
        ai_review = book_review_GPT(book_info)
        st.subheader('・AIによる書評')
        st.write(ai_review)
        st.write('\n')
        st.write('\n')
    except Exception as _: pass