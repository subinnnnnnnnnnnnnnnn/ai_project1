import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

st.set_page_config(page_title="서울 관광지 지도", layout="wide")

st.title("📍 외국인들이 좋아하는 서울 주요 관광지 Top 10")
st.write("지도에서 관광지를 클릭하면 상세 설명이 아래에 나타납니다!")

# 데이터 준비
data = [
    ("경복궁 Gyeongbokgung Palace", 37.5796, 126.9770,
     "조선 시대의 대표 궁궐로 한국 전통 건축미를 상징하는 관광 명소.",
     "경복궁역 (3호선)"),
    ("남산타워 Namsan Seoul Tower", 37.5512, 126.9882,
     "서울을 한눈에 내려다볼 수 있는 전망 명소로 커플 성지로도 유명함.",
     "명동역 (4호선) / 버스환승"),
    ("명동 Myeongdong", 37.5637, 126.9853,
     "쇼핑과 길거리 음식이 많아 외국인이 가장 즐겨 찾는 번화가.",
     "명동역 (4호선)"),
    ("홍대 Hongdae Street", 37.5551, 126.9368,
     "젊음의 예술거리! 버스킹, 카페, 쇼핑 등 감성 가득.",
     "홍대입구역 (2호선 / 경의중앙 / 공항철도)"),
    ("동대문디자인플라자 DDP", 37.5665, 127.0090,
     "자하 하디드가 설계한 미래형 건축 랜드마크.",
     "동대문역사문화공원역 (2·4·5호선)"),
    ("인사동 Insadong Street", 37.5740, 126.9858,
     "전통 차, 공예품, 한복 등 한국 감성을 느낄 수 있는 문화 거리.",
     "안국역 (3호선)"),
    ("북촌한옥마을 Bukchon Hanok Village", 37.5826, 126.9830,
     "한옥이 이어진 아름다운 골목 산책 명소.",
     "안국역 (3호선)"),
    ("롯데월드타워 Lotte World Tower", 37.5131, 127.1029,
     "123층 랜드마크! 쇼핑, 전망대, 호텔, 아쿠아리움까지 한 번에.",
     "잠실역 (2·8호선)"),
    ("청계천 Cheonggyecheon Stream", 37.5690, 126.9784,
     "도심 속 힐링 산책로로 밤이 특히 아름다움.",
     "을지로입구역 (2호선) / 종각역 (1호선)"),
    ("광장시장 Gwangjang Market", 37.5704, 127.0021,
     "빈대떡, 마약김밥으로 알려진 한국 전통 시장.",
     "종로5가역 (1호선)"),
]

df = pd.DataFrame(data, columns=["이름", "위도", "경도", "설명", "가까운 지하철역"])

# 지도 생성
m = folium.Map(location=[37.5665, 126.9780], zoom_start=12)

# 마커 추가 (강조 스타일 적용)
for i, row in df.iterrows():
    folium.Marker(
        location=[row["위도"], row["경도"]],
        popup=row["이름"],
        tooltip=row["이름"],
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(m)

# 지도 표시 + 클릭 이벤트 감지
clicked = st_folium(m, width=900, height=600)

st.write("---")

# 클릭된 관광지 이름 가져오기
selected_place = None
if clicked and clicked["last_object_clicked"]:
    selected_place = clicked["last_object_clicked"].get("popup")

# 선택된 관광지 정보 표시
if selected_place:
    info = df[df["이름"] == selected_place].iloc[0]
    st.subheader(f"🏛️ {info['이름']}")
    st.write(f"**설명**: {info['설명']}")
    st.write(f"**🚇 가장 가까운 지하철역**: {info['가까운 지하철역']}")
else:
    st.write("👆 지도에서 관광지를 클릭하면 상세 정보가 여기에 표시됩니다.")
