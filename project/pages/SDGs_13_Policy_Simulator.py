import os, streamlit as st, numpy as np, pandas as pd, seaborn as sns, matplotlib.pyplot as plt

# 1. 데이터 경로 설정 및 CSV 로드
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
DISASTER_CSV = os.path.join(DATA_DIR, "disaster_data.csv")
disaster_df = pd.read_csv(DISASTER_CSV)

# 2. 국가 리스트 생성
COUNTRY_LIST = disaster_df["country"].unique().tolist()

# 3. 몬테카를로 시뮬레이션 함수 정의
def run_monte_carlo(base_damage, policy_effectiveness=0.1, simulations=1000):
    np.random.seed(42)
    # 정책 효과를 반영한 평균 감소, 약간의 노이즈 추가
    factors = np.random.normal(loc=1 - policy_effectiveness, scale=0.05, size=simulations)
    results = np.maximum(base_damage * factors, 0)  # 피해액은 0 미만 불가
    return results

# 4. Streamlit UI 구성
st.title("🏛️ 정책 시나리오 시뮬레이션")

policy_options = {
    "A안 - 경보 시스템 강화": 0.15,
    "B안 - 하천 정비": 0.25,
    "C안 - 인프라 내진": 0.35
}

country = st.selectbox("국가 선택", COUNTRY_LIST)
policy_name = st.radio("정책 선택", list(policy_options.keys()))
effect = policy_options[policy_name]
runs = st.slider("반복 횟수", 500, 5000, 1000, 500)

base = disaster_df[disaster_df["country"] == country]["damage"].mean()

results = run_monte_carlo(base, policy_effectiveness=effect, simulations=runs)

st.markdown(f"**{policy_name}** 적용 시 평균 피해: **{np.mean(results):,.1f} 억원**")

fig, ax = plt.subplots()
sns.histplot(results, kde=True, ax=ax, color="teal")
ax.set_xlabel("예상 피해액 (억원)")
ax.set_ylabel("빈도")
st.pyplot(fig)

# 용어 및 시뮬레이션 설명
st.markdown("""
**용어 설명:**  
- **예상 피해액**: 정책 효과가 반영된 재난 피해액 예상치 (억원)  
- **반복 횟수**: 몬테카를로 시뮬레이션 반복 실험 횟수

**몬테카를로 시뮬레이션 설명:**  
정책 효과에 따른 피해액 감소 정도를 확률 분포를 이용해 1000회 이상 반복 실험하여,  
불확실성을 정량적으로 평가합니다.  
""")
