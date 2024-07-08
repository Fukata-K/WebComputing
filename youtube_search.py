import streamlit as st
from googleapiclient.discovery import build

YOUTUBE_API_KEY = st.secrets['GOOGLE_API_KEY']


# Youtubeで受け取ったキーワードを検索して結果を返す関数
def search_youtube(keyword):
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    search_responses = youtube.search().list(
        q=keyword,
        part='snippet',
        type='video',
        regionCode="jp",
        maxResults=5,# 5~50まで
    ).execute()

    return search_responses['items']


# 動画の情報を受け取り表示する関数
def display_youtube_info(youtube_info, book_title):

    snippetInfo = youtube_info['snippet']
    title = snippetInfo['title'] # 動画のタイトル
    description = snippetInfo['description'] # 動画の概要
    channel_title = snippetInfo['channelTitle'] # 投稿者
    videoId = youtube_info['id']['videoId']
    videoUrl = f'https://www.youtube.com/watch?v={videoId}'

    if book_title in title or book_title in description:
        st.subheader('・YouTubeでの検索結果')
        st.write('動画のタイトル: ' + title)
        st.write('チャンネル名　: ' + channel_title)
        st.video(videoUrl)
        st.write('\n')
        st.write('\n')