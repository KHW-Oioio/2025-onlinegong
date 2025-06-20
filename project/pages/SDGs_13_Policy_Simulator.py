import os, streamlit as st, numpy as np, pandas as pd, seaborn as sns, matplotlib.pyplot as plt

# 데이터 경로 및 CSV 로드
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
DISASTER_CSV = os.path.join(DATA_DIR, "disaster_data.csv")
disaster_df = pd.read_csv(DISASTER_CSV)

COUNTRY_LIST = disaster_df["country"].unique().tolist()

def run_monte_carlo(base_damage, policy_effectiveness=0.1, simulations=1000):
    np.random.seed(42)
    factors = np.random.normal(loc=1 - policy_effectiveness, scale=0.05, size=simulations)
    results = np.maximum(base_damage * factors, 0)
    return results

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

st.markdown(f"### 💡 정책 효과 분석 결과")
st.markdown(f"- 선택된 국가: **{country}**")
st.markdown(f"- 적용된 정책: **{policy_name}** (피해 감소 예상치: 약 {effect*100:.0f}%)")
st.markdown(f"- 몬테카를로 시뮬레이션 반복 횟수: **{runs}회**")
st.markdown(f"- 정책 적용 후 평균 예상 피해액: **{np.mean(results):,.1f} 억원** (기존 평균 피해액: {base:.1f} 억원)")

fig, ax = plt.subplots()
sns.histplot(results, kde=True, ax=ax, color="teal")
ax.set_xlabel("예상 피해액 (억원)")
ax.set_ylabel("빈도")
ax.set_title(f"{policy_name} 적용 시 예상 피해액 분포")
st.pyplot(fig)

st.markdown("""
---
### 📘 그래프 해석 가이드  
- 히스토그램은 몬테카를로 시뮬레이션 결과, 정책이 적용된 후 예상 피해액이 어떻게 분포하는지 보여줍니다.  
- 그래프의 오른쪽 꼬리가 길면 큰 피해 발생 가능성도 있다는 의미입니다.  
- 평균 피해액은 그래프 중앙의 분포 평균이며, 정책 효과가 클수록 평균이 더 낮아집니다.  
- 정책의 효과값은 피해를 줄이는 비율이며, 예: 0.25는 25% 피해 감소 예상을 뜻합니다.  

### ⚙️ 몬테카를로 시뮬레이션 설명  
- 실제 재난 피해액은 여러 불확실성 때문에 일정하지 않고 분포를 가집니다.  
- 시뮬레이션은 이런 불확실성을 확률 분포로 모사해 여러 번 실험 후 결과를 분석합니다.  
- 이를 통해 정책 도입 시 예상 피해액 범위와 평균 효과를 직관적으로 확인할 수 있습니다.  
""")
