import streamlit as st
import requests

REQUEST_URL = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706"
APP_ID = st.secrets["RAKUTEN_APP_ID"]


# 楽天市場で与えられたキーワードの検索を行い商品情報を返す関数
def search_rakuten(search_keyword):
    search_params = {
        "format" : "json",
        "keyword" : search_keyword,
        "applicationId" : [APP_ID],
        "availability" : 0,
        "hits" : 1,
        "page" : 1,
        "sort" : "standard"
    }

    response = requests.get(REQUEST_URL, search_params)
    result = response.json()
    
    return result["Items"][0]["Item"]


# item_infoを受け取り表示する関数
def display_rakuten_info(item_info):
    st.subheader('・楽天市場での検索結果')
    
    try: st.write('商品名: ', item_info['itemName'])
    except KeyError as _: pass
    
    try: st.write('値段　: ', str(item_info['itemPrice']) + "円")
    except KeyError as _: pass

    try: st.write('楽天のリンク: ', item_info['itemUrl'])
    except KeyError as _: pass
    
    try: st.image(item_info['smallImageUrls'][0]['imageUrl'], '商品の画像')
    except Exception as _: pass
    
    st.write('\n')
    st.write('\n')