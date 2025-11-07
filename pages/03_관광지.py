import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="서울 관광지 지도", layout="wide")

st.title("📍 외국인들이 좋아하는 서울 주요 관광지 Top 10")
st.write("서울의 인기 관광지를 지도에서 확인해보세요!")

# 서울 관광지 Top 10 (이름, 위도, 경도)
locations = [
    ("경복궁 Gyeongbokgung Palace", 37.5796, 126.9770),
    ("남산타워 Namsan Seoul Tower", 37.5512, 126.9882),
    ("명동 Myeongdong", 37.5637, 126.9853),
    ("홍대 Hongdae Street", 37.5551, 126.9368),
    ("동대문디자인플라자 DDP", 37.5665, 127.0090),
    ("인사동 Insadong Street", 37.5740, 126.9858),
    ("북촌한옥마을 Bukchon Hanok Village", 37.5826, 126.9830),
    ("롯데월드타워 Lotte World Tower", 37.5131, 127.1029),
    ("청계천 Cheonggyecheon Stream", 37.5690, 126.9784),
    ("광장시장 Gwangjang Market", 37.5704, 127.0021),
]

# 지도 생성
m = folium.Map(location=[37.5665, 126.9780], zoom_start=12)

# 마커 추가
for name, lat, lon in locations:
    folium.Marker(
        location=[lat, lon],
        popup=name,
        tooltip=name
    ).add_to(m)

# 지도 출력
st_data = st_folium(m, width=900, height=600)

st.write("---")
st.write("🗺️ 지도를 확대/이동하며 여행 계획에 참고해보세요!")
