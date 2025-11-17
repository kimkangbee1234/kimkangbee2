import streamlit as st
import pandas as pd
import numpy as np

st.title("📊 줄기와 잎 그림 & 도수분포표")

# 데이터 입력
st.write("자료를 쉼표(,)로 구분하여 입력하세요. 예: 12, 14, 16, 17, 19, 22, 24, 25, 29, 30")
data_input = st.text_area("자료 입력", "12, 14, 16, 17, 19, 22, 24, 25, 29, 30")

# 계급폭 선택 (5 또는 10)
bin_width = st.radio("계급폭을 선택하세요", [5, 10])

try:
    # 데이터 정리
    data = sorted([int(x.strip()) for x in data_input.split(",") if x.strip() != ""])
    min_val, max_val = min(data), max(data)

    # 기준을 0 또는 10단위로 정렬
    start = (min_val // bin_width) * bin_width
    end = ((max_val // bin_width) + 1) * bin_width

    # 계급 경계 생성
    bins = np.arange(start, end + bin_width, bin_width)

    # 도수 계산
    counts, bin_edges = np.histogram(data, bins=bins)
    df = pd.DataFrame({
        "계급": [f"{int(bin_edges[i])} - {int(bin_edges[i+1])}" for i in range(len(counts))],
        "도수": counts
    })

    st.subheader("📋 도수분포표")
    st.dataframe(df, use_container_width=True)

    # 줄기와 잎 그림
    st.subheader("🌿 줄기와 잎 그림")
    st.write("※ 줄기는 십의 자리, 잎은 일의 자리로 나누어 표시됩니다.")

    # 줄기와 잎 나누기
    stems = {}
    for num in data:
        stem = num // 10
        leaf = num % 10
        if stem not in stems:
            stems[stem] = []
        stems[stem].append(leaf)

    for stem, leaves in stems.items():
        leaves_str = " ".join(str(l) for l in sorted(leaves))
        st.write(f"**{stem} |** {leaves_str}")

except Exception as e:
    st.error(f"⚠️ 오류가 발생했습니다: {e}")