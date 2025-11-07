import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

st.set_page_config(page_title="서울 관광지 지도", layout="wide")

st.title("📍 외국인들이 좋아하는 서울 주요 관광지 Top 10")
st.write("서울의 인기 관광지를 한눈에 보고, 설명과 가장 가까운 지하철역 정보를 확인해보세요!")

# 관광지 데이터 (이름, 위도, 경도, 설명, 지하철역)
data = [
    ("경복궁 Gyeongbokgung Palace", 37.5796, 126.9770,
     "조선 시대의 대표 궁궐로 한국 전통 건축미를 상징하는 관광 명소.",
     "경복궁역 (3호선)"),
    ("남산타워 Namsan Seoul Tower", 37.5512, 126.9882,
     "서울을 한눈에 내려다볼 수 있는 전망 명소로 커플 성지로도 유명함.",
     "명동역 (4호선) / 버스환승"),
    ("명동 Myeongdong", 37.5637, 126.9853,
     "쇼핑과 다양한 먹거리가 가득해 외국인에게 가장 인기 있는 번화가.",
     "명동역 (4호선)"),
    ("홍대 Hongdae Street", 37.5551, 126.9368,
     "젊음의 거리! 스트릿공연, 카페, 클럽이 몰려있는 예술적 분위기.",
     "홍대입구역 (2호선 / 경의중앙 / 공항철도)"),
    ("동대문디자인플라자 DDP", 37.5665, 127.0090,
     "자하 하디드가 설계한 미래형 건축물로 전시·행사·포토스팟 성지.",
     "동대문역사문화공원역 (2·4·5호선)"),
    ("인사동 Insadong Street", 37.5740, 126.9858,
     "전통 공예품, 한복, 한국적 분위기를 느낄 수 있는 문화 거리.",
     "안국역 (3호선)"),
    ("북촌한옥마을 Bukchon Hanok Village", 37.5826, 126.9830,
     "전통 한옥 골목 풍경이 아름다워 산책 명소로 인기.",
     "안국역 (3호선)"),
    ("롯데월드타워 Lotte World Tower", 37.5131, 127.1029,
     "123층 초고층 타워! 쇼핑, 전망대, 호텔, 아쿠아리움까지 한 곳에.",
     "잠실역 (2·8호선)"),
    ("청계천 Cheonggyecheon Stream", 37.5690, 126.9784,
     "도심 속 힐링 산책로로 밤 조명으로 더욱 아름다움.",
     "을지로입구역 (2호선) / 종각역 (1호선)"),
    ("광장시장 Gwangjang Market", 37.5704, 127.0021,
     "한국 전통 시장으로 빈대떡과 마약김밥으로 유명함.",
     "종로5가역 (1호선)"),
]

df = pd.DataFrame(data, columns=["이름", "위도", "경도", "설명", "가까운 지하철역"])

# 지도 생성
m = folium.Map(location=[37.5665, 126.9780], zoom_start=12)

# 마커 추가 (더 눈에 띄게 → CircleMarker 사용)
for name, lat, lon, desc, subway in data:
    folium.CircleMarker(
        location=[lat, lon],
        radius=8,
        popup=f"<b>{name}</b><br>{desc}<br><i>🚇 가까운 역: {subway}</i>",
        tooltip=name,
        weight=3,
        fill=True
    ).add_to(m)

# 지도 출력
st_folium(m, width=900, height=600)

st.write("---")
st.subheader("📖 관광지 설명 & 지하철 정보")

st.dataframe(df[["이름", "설명", "가까운 지하철역"]])
