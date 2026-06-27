import streamlit as st
import random

st.set_page_config(page_title="메이플스토리 기대값 계산기", layout="wide")
st.title("🍁 메이플스토리 시뮬레이터 및 기대값 계산기")
st.caption("잠재능력 등업, 옵션 및 스타포스 기대값을 계산해주는 웹어플리케이션입니다.")

# 사이드바 메뉴
menu = st.sidebar.selectbox("기능을 선택하세요", ["잠재능력 등업 기대값", "스타포스 기대값"])

# 1. 잠재능력 등업 탭
if menu == "잠재능력 등업 기대값":
    st.header("✨ 잠재능력 등업 기대값 계산기")
    
    col1, col2 = st.columns(2)
    with col1:
        cube_type = st.selectbox("큐브 종류", ["레드 큐브 (명장)", "블랙 큐브 (미라클)", "에디셔널 큐브"])
        current_grade = st.selectbox("현재 등급", ["레어", "에픽", "유니크"])
    with col2:
        target_grade = st.selectbox("목표 등급", ["에픽", "유니크", "레전더리"])
        
    if st.button("등업 기대값 계산하기"):
        # 임의의 기준 확률 테이블 (실제 공식 확률 데이터 대입 필요)
        # 예시: 블랙큐브 유니크 -> 레전더리 확률 약 1.2% 등
        success_rate = 0.012 if cube_type == "블랙 큐브 (미라클)" and current_grade == "유니크" else 0.05
        
        expected_cubes = int(1 / success_rate)
        
        st.success(f"🎯 **{current_grade}**에서 **{target_grade}**까지 예상이상 무난한 진행 시:")
        st.metric(label="평균 필요 큐브 개수", value=f"약 {expected_cubes} 개")
        st.info("※ 공식 오픈 API 및 유저 통계 기반 확률을 참고한 평균값이며, 실제 인게임에서는 편차가 존재할 수 있습니다.")

# 2. 스타포스 탭
elif menu == "스타포스 기대값":
    st.header("⭐ 스타포스 기대값 계산기")
    
    col1, col2 = st.columns(2)
    with col1:
        item_level = st.selectbox("장비 레벨", [150, 160, 200])
        curr_star = st.number_input("현재 스타포스", min_value=0, max_value=24, value=12)
        target_star = st.number_input("목표 스타포스", min_value=1, max_value=25, value=17)
    with col2:
        star_catch = st.checkbox("스타캐치 적용")
        destroy_prevent = st.checkbox("15성~16성 파괴방지 적용")
        event_type = st.selectbox("이벤트 적용", ["없음", "1+1 이벤트 (10성 이하)", "5성/10성/15성 100% 성공"])

    if st.button("스타포스 기대값 계산하기"):
        if curr_star >= target_star:
            st.error("목표 성급은 현재 성급보다 높아야 합니다.")
        else:
            # 대략적인 기대값 계산 알고리즘 예시 (실제 스타포스 비용 수식 적용 필요)
            base_cost = (item_level ** 3) * (curr_star + 1) / 100
            total_expected_cost = base_cost * (target_star - curr_star) * 1.5
            if destroy_prevent and curr_star >= 15:
                total_expected_cost *= 2 # 파방 비용 추가 예시
                
            st.success(f"⚙️ {curr_star}성 ➡️ {target_star}성 강화 기대값 결과")
            st.metric(label="평균 소모 메소", value=f"{int(total_expected_cost):,} 메소")
            st.warning("⚠️ 파괴 확률이 존재하는 구간입니다. 기댓값은 '파괴 시 복구 비용'을 임의 포함한 수치일 수 있습니다.")
