"""
Streamlit app: MBTI by Country (Plotly)
- Reads CSV from /mnt/data/countriesMBTI_16types (1).csv by default (you can also upload your own CSV)
- Interactive Plotly bar chart: when you pick a country, shows MBTI distribution
- Coloring: top type = red, others = blue gradient (darker = higher)
- Provides the app source code for easy copy and a downloadable requirements.txt

Run:
    streamlit run streamlit_mbti_plotly_app.py

Make sure requirements (provided in-app) include: streamlit, pandas, plotly
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import io

# ----------------------
# App configuration
# ----------------------
st.set_page_config(page_title="MBTI by Country — Interactive", layout="wide")
st.title("🌏 MBTI 분포 — 국가별 시각화 (Plotly)")
st.markdown("선택한 국가의 MBTI 비율을 깔끔하고 인터랙티브한 막대그래프로 보여줍니다.")

# ----------------------
# Load data
# ----------------------
DEFAULT_PATH = "/mnt/data/countriesMBTI_16types (1).csv"
uploaded = st.sidebar.file_uploader("CSV 파일 업로드 (선택) — 아니면 기본 데이터 사용", type=["csv"])

@st.cache_data
def load_data(uploaded_file):
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
        except Exception:
            df = pd.read_csv(uploaded_file, encoding="utf-8-sig")
    else:
        try:
            df = pd.read_csv(DEFAULT_PATH)
        except Exception as e:
            st.error(f"기본 파일 로드 실패: {e}")
            return None
    return df

with st.spinner("데이터 불러오는 중..."):
    df = load_data(uploaded)

if df is None:
    st.stop()

# Normalize column names (strip)
df.columns = [c.strip() for c in df.columns]

# identify MBTI columns (assume all except 'Country')
if 'Country' not in df.columns:
    st.error("CSV 파일에 'Country' 열이 필요합니다.")
    st.stop()

mbti_cols = [c for c in df.columns if c != 'Country']

# Ensure MBTI columns are numeric
for c in mbti_cols:
    df[c] = pd.to_numeric(df[c], errors='coerce')

# Basic checks
if df[mbti_cols].isnull().any().any():
    st.warning("데이터에 NaN 값이 포함되어 있습니다. 해당 값은 0으로 처리해 시각화합니다.")
    df[mbti_cols] = df[mbti_cols].fillna(0)

# Sidebar controls
st.sidebar.markdown("---")
country_list = df['Country'].tolist()
selected_country = st.sidebar.selectbox('국가 선택', country_list, index=0)

# Option to sort MBTI types
sort_option = st.sidebar.radio('정렬 방식', options=['원래 순서', '비율 내림차순'], index=1)

# ----------------------
# Prepare data for selected country
# ----------------------
row = df[df['Country'] == selected_country]
if row.empty:
    st.error("선택한 국가의 데이터가 없습니다.")
    st.stop()

values = row[mbti_cols].iloc[0]
plot_df = pd.DataFrame({'MBTI': mbti_cols, 'Ratio': values.values})

if sort_option == '비율 내림차순':
    plot_df = plot_df.sort_values('Ratio', ascending=False)

# Coloring: top = red, others = blue gradient
# Find index of top
top_idx = plot_df['Ratio'].idxmax()

# Generate blue gradient (light to darker) based on relative ratio
# We'll use a simple interpolation between two blue hex values
from math import isnan

min_val = plot_df['Ratio'].min()
max_val = plot_df['Ratio'].max()

# helper to interpolate colors
def lerp(a, b, t):
    return int(a + (b - a) * t)

# blue range: light blue to dark blue
light_blue = (220, 235, 252)  # RGB
dark_blue  = (10, 70, 160)
red_rgb = (255, 65, 54)

colors = []
for i, r in enumerate(plot_df['Ratio']):
    if r == plot_df['Ratio'].max():
        colors.append('rgb({}, {}, {})'.format(*red_rgb))
    else:
        # normalize between 0..1
        t = 0.0 if max_val==min_val else (r - min_val) / (max_val - min_val)
        # invert t so larger values are darker
        t = t
        R = lerp(light_blue[0], dark_blue[0], t)
        G = lerp(light_blue[1], dark_blue[1], t)
        B = lerp(light_blue[2], dark_blue[2], t)
        colors.append('rgb({}, {}, {})'.format(R, G, B))

# ----------------------
# Plotly bar chart
# ----------------------
fig = px.bar(
    plot_df,
    x='MBTI',
    y='Ratio',
    text=plot_df['Ratio'].apply(lambda x: f"{x:.2%}"),
    labels={'Ratio': '비율', 'MBTI': 'MBTI 유형'},
    title=f"{selected_country} — MBTI 분포",
)

fig.update_traces(marker_color=colors, textposition='outside', marker_line_color='rgb(8,48,107)', marker_line_width=0.5)
fig.update_layout(yaxis_tickformat=".0%", uniformtext_minsize=10, uniformtext_mode='show', margin=dict(l=40, r=40, t=70, b=40))

# Make plot responsive
fig.update_layout(autosize=True)

# Show main area: chart + description
left, right = st.columns([3, 1])
with left:
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.markdown("### 🔎 선택한 국가 정보")
    st.write(f"**국가**: {selected_country}")
    top_row = plot_df.iloc[0]
    top_type = plot_df.loc[plot_df['Ratio'].idxmax(), 'MBTI']
    top_value = plot_df['Ratio'].max()
    st.write(f"**가장 높은 MBTI**: {top_type} — {top_value:.2%}")
    st.write("\n**상위 5 MBTI**")
    st.dataframe(plot_df.head(5).assign(Ratio=lambda d: d['Ratio'].apply(lambda x: f"{x:.2%}")))

# ----------------------
# Provide code and requirements for easy copy/download
# ----------------------
st.markdown("---")
st.header("앱 소스 코드 (복사/다운로드 가능)")

# Read this file's source to show in the app (best-effort)
try:
    with open(__file__, 'r', encoding='utf-8') as f:
        source = f.read()
except Exception:
    # fallback: reconstruct a short message
    source = "(앱 실행 환경에서는 소스 파일을 직접 보여줄 수 없습니다. Git/로컬 파일을 확인하세요.)"

st.code(source, language='python')

# Download buttons
py_bytes = source.encode('utf-8')
requirements_txt = "streamlit\npandas\nplotly\n"

st.download_button("🡇 streamlit_mbti_plotly_app.py 다운로드", data=py_bytes, file_name="streamlit_mbti_plotly_app.py", mime='text/x-python')
st.download_button("🡇 requirements.txt 다운로드", data=requirements_txt, file_name="requirements.txt", mime='text/plain')

st.markdown("---")
st.caption("앱은 Streamlit Cloud에서 잘 작동합니다. (streamlit run streamlit_mbti_plotly_app.py)")
