import streamlit as st
import requests
import xml.etree.ElementTree as ET

st.set_page_config(page_title="한국어 사전 검색", layout="wide")

API_KEY = "여기에_너의_API_KEY_입력"  # ❗ 반드시 본인 키로 변경해주세요

st.title("📘 한국어 사전 검색 (표준국어대사전 API 연동)")
st.write("‘모든 한국어 단어 전체’를 검색할 수 있는 표준국어대사전 기반 검색 서비스입니다.")

query = st.text_input("🔍 검색할 단어를 입력하세요:")

if query:
    url = f"https://opendict.korean.go.kr/api/search?key={API_KEY}&q={query}&req_type=json"

    response = requests.get(url)

    if response.status_code == 200:
        try:
            data = response.json()

            if "channel" in data and "item" in data["channel"]:
                items = data["channel"]["item"]

                st.success(f"'{query}' 검색 결과 {len(items)}개")

                for item in items:
                    word = item.get("word", "(단어 없음)")
                    pos = item.get("pos", "(품사 없음)")
                    definition = item.get("sense", {}).get("definition", "(뜻 없음)")
                    origin = item.get("sense", {}).get("origin", "(어원 정보 없음)")

                    st.markdown(f"""
                    ### 🔵 {word}
                    **품사:** {pos}  
                    **뜻:** {definition}  
                    **어원:** {origin}  
                    ---  
                    """)
            else:
                st.error("검색 결과가 없습니다.")

        except:
            st.error("검색 처리 중 오류가 발생했습니다.")
    else:
        st.error("API 응답 오류 발생")

else:
    st.info("단어를 입력하면 뜻 · 품사 · 설명 · 어원 정보가 표시됩니다!")
