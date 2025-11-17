import streamlit as st
import pandas as pd
import numpy as np

st.title("📊 줄기와 잎 그림 & 도수분포표")

# --- 예시 데이터 버튼 ---
col1, col2, col3, col4 = st.columns(4)

example_data = ""

with col1:
    if st.button("예시 1"):
        example_data = "32,79,51,61,65,40,53,46,78,64,54,62,70,43,68,64,48,39,72,77"
with col2:
    if st.button("예시 2"):
        example_data = "87,79,90,68,94,91,88,83,69,90,71,87,65,89,93,91,78,76,80,80,79,93,73,84"
with col3:
    if st.button("예시 3"):
        example_data = "15,15,9,12,12,18,10,15,20,21,11,11,12,13,7,8,13,13,29,10"
with col4:
    if st.button("직접 입력"):
        example_data = ""

# --- 데이터 입력창 ---
data_input = st.text_area(
    "자료 입력",
    value=example_data,
    placeholder="값을 쉼표(,)로 구분해 입력하세요. 예: 45, 50, 60, 70, 80"
)

# --- 계급폭 선택 ---
bin_width = st.radio("계급폭을 선택하세요", [5, 10])

# --- 처리 및 출력 ---
try:
    # 아무것도 입력 안 했을 때 예외 처리
    if not data_input.strip():
        st.warning("자료를 입력하거나 예시를 선택하세요.")
    else:
        data = sorted([int(x.strip()) for x in data_input.split(",") if x.strip().isdigit()])
        if len(data) == 0:
            st.warning("유효한 숫자 데이터를 입력하세요.")
        else:
            # 계급 범위 계산
            min_val, max_val = min(data), max(data)
            start = (min_val // bin_width) * bin_width
            end = ((max_val // bin_width) + 1) * bin_width
            bins = np.arange(start, end + bin_width, bin_width)

            # 도수분포표 생성
            counts, bin_edges = np.histogram(data, bins=bins)
            df = pd.DataFrame({
                "계급": [f"{int(bin_edges[i])} - {int(bin_edges[i+1])}" for i in range(len(counts))],
                "도수": counts
            })

            st.subheader("📋 도수분포표")
            st.dataframe(df, use_container_width=True)

            # 줄기와 잎 그림 생성
            st.subheader("🌿 줄기와 잎 그림")
            st.write("※ 줄기는 십의 자리, 잎은 일의 자리로 나누어 표시됩니다.")

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