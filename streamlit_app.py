import streamlit as st
import pandas as pd
import numpy as np

st.title("📊 줄기와 잎 그림 & 도수분포표")

# --- 세션 상태 초기화 ---
if 'input_data' not in st.session_state:
    st.session_state['input_data'] = ""

def set_data(data_str):
    st.session_state['input_data'] = data_str

# --- 예시 데이터 버튼 ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.button("예시 1", on_click=set_data, args=("32,79,51,61,65,40,53,46,78,64,54,62,70,43,68,64,48,39,72,77",))
with col2:
    st.button("예시 2", on_click=set_data, args=("87,79,90,68,94,91,88,83,69,90,71,87,65,89,93,91,78,76,80,80,79,93,73,84",))
with col3:
    st.button("예시 3", on_click=set_data, args=("15,15,9,12,12,18,10,15,20,21,11,11,12,13,7,8,13,13,29,10",))
with col4:
    st.button("직접 입력", on_click=set_data, args=("",))

# --- 데이터 입력창 ---
data_input = st.text_area(
    "자료 입력",
    key="input_data",
    placeholder="값을 쉼표(,)로 구분해 입력하세요."
)

# --- 계급폭 선택 ---
bin_width = st.radio("계급폭을 선택하세요", [5, 10])

# --- 처리 및 출력 ---
try:
    if not data_input.strip():
        st.warning("자료를 입력하거나 예시를 선택하세요.")
    else:
        # 1. 데이터를 먼저 해석합니다.
        data = sorted([int(x.strip()) for x in data_input.split(",") if x.strip().isdigit()])
        
        if len(data) == 0:
            st.warning("유효한 숫자 데이터를 입력하세요.")
        else:
            # 2. [위치 변경] 계급폭 선택 바로 밑에 데이터 정보를 출력합니다.
            st.info(f"**변량의 개수:** 총 {len(data)}개")
            
            # -------------------------------------------------------

            # 3. 그 다음 도수분포표 계산 및 출력
            min_val, max_val = min(data), max(data)
            start = (min_val // bin_width) * bin_width
            end = ((max_val // bin_width) + 1) * bin_width
            bins = np.arange(start, end + bin_width, bin_width)
            counts, bin_edges = np.histogram(data, bins=bins)
            
            labels = [f"{int(bin_edges[i])} - {int(bin_edges[i+1])}" for i in range(len(counts))]
            df = pd.DataFrame({"계급": labels, "도수": counts})

            st.subheader("📋 도수분포표")
            st.dataframe(df, use_container_width=True)

            # 4. 줄기와 잎 그림 출력
            st.subheader("🌿 줄기와 잎 그림")
            
            stems = {}
            for num in data:
                stem = num // 10
                leaf = num % 10
                if stem not in stems:
                    stems[stem] = []
                stems[stem].append(leaf)

            sorted_stems = sorted(stems.keys())
            
            for stem in sorted_stems:
                leaves = stems[stem]
                leaves_str = " ".join(str(l) for l in sorted(leaves))
                
                # [수정됨] margin-bottom: 10px; 추가 -> 줄 간격 벌리기
                st.markdown(
                    f"<div style='font-size: 18px; margin-bottom: 10px;'>{stem} &nbsp;| &nbsp; {leaves_str}</div>", 
                    unsafe_allow_html=True
                )

except Exception as e:
    st.error(f"⚠️ 오류가 발생했습니다: {e}")