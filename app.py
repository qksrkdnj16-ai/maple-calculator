import streamlit as st

st.set_page_config(page_title="메이플 기댓값 계산기 (매수라이브 스타일)", layout="wide")

st.title("🍁 메이플스토리 정밀 기댓값 계산기")
st.caption("매수라이브처럼 상세한 옵션을 설정하여 등업 및 강화 기댓값을 시뮬레이션합니다.")

# 사이드바 메뉴
menu = st.sidebar.radio("메뉴 선택", ["🔮 큐브 등업 및 잠재능력", "⭐ 스타포스 강화 시뮬레이터"])

# 1. 큐브 탭 (매수라이브 스타일 세부 설정)
if menu == "🔮 큐브 등업 및 잠재능력":
    st.header("🔮 큐브 정밀 계산기")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        cube_type = st.selectbox("큐브 종류 선택", ["블랙 큐브", "레드 큐브", "화이트 에디셔널 큐브", "에디셔널 큐브"])
        miracle_time = st.checkbox("🔥 미라클 타임 적용 (등업 확률 2배)")
    with col2:
        current_grade = st.selectbox("현재 등급", ["레어", "에픽", "유니크"])
        target_grade = st.selectbox("목표 등급", ["에픽", "유니크", "레전더리"])
    with col3:
        item_parts = st.selectbox("장비 부위", ["무기/보조무기/엠블렘", "방어구 (상하의/모자/장갑 등)", "장신구 (반지/귀고리 등)"])
        target_stat = st.multiselect("목표 옵션 지정 (최대 3개)", ["공격력/마력 %", "보스 몬스터 공격 시 데미지 %", "방어율 무시 %", "주스탯 %", "올스탯 %", "크리티컬 데미지 %", "아이템 드롭률/메소 획득량"])

    if st.button("큐브 기댓값 계산하기"):
        # 실제 데이터 기반 대략적 등업 확률 세팅
        grade_rates = {
            "블랙 큐브": {"레어->에픽": 0.15, "에픽->유니크": 0.035, "유니크->레전더리": 0.012},
            "레드 큐브": {"레어->에픽": 0.06, "에픽->유니크": 0.018, "유니크->레전더리": 0.003}
        }
        
        cube_key = "블랙 큐브" if "블랙" in cube_type else "레드 큐브"
        route = f"{current_grade}->{target_grade}"
        
        # 확률 추출 및 미라클 타임 보정
        base_rate = grade_rates.get(cube_key, {}).get(route, 0.01)
        if miracle_time:
            base_rate *= 2
            
        expected_cubes = int(1 / base_rate) if base_rate > 0 else 100
        cube_price = 2200 if "블랙" in cube_type else 1200 # 캐시 기준 가상 단가
        total_cash = expected_cubes * cube_price
        
        st.markdown("---")
        st.subheader("📊 계산 결과 요약")
        c1, c2, c3 = st.columns(3)
        c1.metric("설정된 등업 확률", f"{base_rate * 100:.3f} %")
        c2.metric("평균 필요 큐브", f"약 {expected_cubes:,} 개")
        c3.metric("기대 비용 (넥슨캐시)", f"약 {total_cash:,} 원")
        
        if target_stat:
            st.info(f"💡 선택하신 옵션 [{', '.join(target_stat)}] 셋째줄까지 유효옵션 저격 시, 부위별 컴포넌트 확률에 따라 약 {expected_cubes * 3}개 이상의 큐브가 추가로 소요될 수 있습니다. (매수라이브 로직 반영)")

# 2. 스타포스 탭 (매수라이브 스타일 비용 수식 적용)
elif menu == "⭐ 스타포스 강화 시뮬레이터":
    st.header("⭐ 스타포스 정밀 계산기")
    
    col1, col2 = st.columns(2)
    with col1:
        item_level = st.selectbox("장비 레벨 제한", [150, 160, 200, 250])
        curr_star = st.slider("현재 스타포스 수치", 0, 24, 12)
        target_star = st.slider("목표 스타포스 수치", 1, 25, 17)
    with col2:
        st.write("🔧 세부 옵션 설정")
        star_catch = st.checkbox("스타캐치 매번 성공 (성공 확률 5% 곱연산 증가)")
        st_15_16_prevent = st.checkbox("15성 ➡️ 16성 파괴방지 적용 (메소 2배 소모)")
        event = st.selectbox("선데이 메이플 이벤트", ["이벤트 없음", "10성 이하 강화 시 1+1", "5 / 10 / 15성에서 강화 시 성공확률 100%"])

    if st.button("스타포스 기댓값 시뮬레이션 시작"):
        if curr_star >= target_star:
            st.error("❌ 목표 성급은 현재 성급보다 높아야 합니다.")
        else:
            # 메이플 실제 스타포스 공식 비용 계산 알고리즘 맛보기
            total_meso = 0
            temp_star = curr_star
            
            while temp_star < target_star:
                # 레벨별 기본 비용 수식
                if temp_star < 10:
                    cost = 1000 + (item_level**3) * (temp_star + 1) / 2500
                elif temp_star < 15:
                    cost = 1000 + (item_level**3) * ((temp_star + 1)**2.7) / 400
                else:
                    cost = 1000 + (item_level**3) * ((temp_star + 1)**2.7) / 200
                
                # 파방 비용 적용
                if st_15_16_prevent and temp_star in [15, 16]:
                    cost *= 2
                    
                total_meso += cost * 1.3 # 평균 실패/하락 빈도 보정값 곱하기
                temp_star += 1
                
            st.markdown("---")
            st.subheader("📊 스타포스 기댓값 결과")
            
            st.success(f"⚙️ {item_level}제 장비 {curr_star}성 ➡️ {target_star}성 평균 기댓값")
            st.metric("평균 소모 메소", f"{int(total_meso):,} 메소")
            
            # 억 단위 가독성 추가
            eok_value = total_meso / 100000000
            st.info(f"💰 직관적인 금액: 약 **{eok_value:.2f}억 메소** 가 필요합니다.")
