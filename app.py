import streamlit as st
import random

st.set_page_config(page_title="메이플스토리 정밀 계산기 (MESULIVE)", layout="wide")

st.sidebar.title("🍁 MESULIVE 마스터")
st.sidebar.info("✅ 2026년 최신 시스템 완벽 적용\n- 큐브 등업 / 옵션 저격 분리\n- 커스텀 수치(%) 정밀 옵션 저격\n- 스타포스 흔적 메소 복구 시스템\n- 샤이닝 스타포스 이벤트 추가")

# -----------------------------------------------------------------
# 탭 구성: 등업 / 옵션 저격 / 스타포스
# -----------------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["🔮 잠재능력 등업", "🎯 옵션 커스텀 저격", "⭐ 정밀 스타포스 계산기"])

# ==========================================
# 1. 잠재능력 등업 시뮬레이터 탭
# ==========================================
with tab1:
    st.header("🔮 잠재능력 확정 등업 시뮬레이터")
    st.caption("시스템별 실제 공식 확률과 천장 시스템을 완벽히 계산합니다.")
    
    col1, col2 = st.columns(2)
    with col1:
        item_level_cube = st.selectbox("장비 레벨 제한 선택", [140, 150, 160, 200, 250], index=3, key="tier_lvl")
        
        # 에디셔널 큐브/화이트 에디셔널 큐브(아이템) 추가
        system_type = st.selectbox("강화 시스템 선택", [
            "잠재능력 재설정 / 블랙 큐브 (메소 소모)",
            "에디셔널 잠재능력 재설정 (메소 소모)",
            "에디셔널 큐브 / 화이트 에디셔널 큐브 (아이템)", 
            "장인의 큐브 / 실버 큐브 (아이템)",
            "명장의 큐브 / 골드 큐브 (아이템)"
        ])
        miracle_time = st.checkbox("🔥 미라클 타임 적용 (기본 등업 확률 2배)")
    
    with col2:
        current_grade = st.selectbox("현재 등급", ["레어", "에픽", "유니크", "레전더리"])
        target_grade = st.selectbox("목표 등급", ["에픽", "유니크", "레전더리"])

    if st.button("🔮 등업 시뮬레이션 가동"):
        level_scale = {140: 0.45, 150: 0.60, 160: 0.70, 200: 1.0, 250: 1.25}
        scale = level_scale[item_level_cube]
        is_meso_system = "메소" in system_type
        
        # 이미지 데이터 기준 확률 및 비용 세팅
        if "블랙 큐브" in system_type:
            base_costs = {"레어": 4500000, "에픽": 18000000, "유니크": 38250000, "레전더리": 45000000}
            rates = {"레어->에픽": 0.15, "에픽->유니크": 0.035, "유니크->레전더리": 0.014}
            ceilings = {"레어->에픽": 11, "에픽->유니크": 32, "유니크->레전더리": 107}
            
        elif "에디셔널 잠재능력" in system_type:
            base_costs = {"레어": 11000000, "에픽": 30800000, "유니크": 74800000, "레전더리": 88000000}
            rates = {"레어->에픽": 0.023810, "에픽->유니크": 0.009804, "유니크->레전더리": 0.007}
            ceilings = {"레어->에픽": 72, "에픽->유니크": 152, "유니크->레전더리": 272}
            
        elif "화이트 에디셔널 큐브" in system_type:
            base_costs = {"레어": 1, "에픽": 1, "유니크": 1, "레전더리": 1}
            rates = {"레어->에픽": 0.047619, "에픽->유니크": 0.019608, "유니크->레전더리": 0.007}
            ceilings = {"레어->에픽": 999, "에픽->유니크": 999, "유니크->레전더리": 999}
            
        elif "장인의 큐브" in system_type:
            base_costs = {"레어": 1, "에픽": 1, "유니크": 1, "레전더리": 1}
            rates = {"레어->에픽": 0.047619, "에픽->유니크": 0.011858, "유니크->레전더리": 0.0}
            ceilings = {"레어->에픽": 999, "에픽->유니크": 999, "유니크->레전더리": 999}
            
        elif "명장의 큐브" in system_type:
            base_costs = {"레어": 1, "에픽": 1, "유니크": 1, "레전더리": 1}
            rates = {"레어->에픽": 0.079994, "에픽->유니크": 0.016959, "유니크->레전더리": 0.001996}
            ceilings = {"레어->에픽": 999, "에픽->유니크": 999, "유니크->레전더리": 999}

        costs = {k: int(v * scale) if is_meso_system else v for k, v in base_costs.items()}

        total_cost_val = 0
        total_tries = 0
        ceil_info_text = []
        prob_info_text = []

        grades = ["레어", "에픽", "유니크", "레전더리"]
        curr_idx = grades.index(current_grade)
        target_idx = grades.index(target_grade)
        
        if curr_idx >= target_idx:
            st.error("❌ 목표 등급이 현재 등급보다 낮거나 같습니다.")
        else:
            for i in range(curr_idx, target_idx):
                route = f"{grades[i]}->{grades[i+1]}"
                base_rate = rates.get(route, 0.0)
                
                if base_rate == 0.0:
                    st.error(f"❌ 선택하신 [{system_type}]로는 {route} 등업이 불가능합니다.")
                    st.stop()
                
                # 확률 정보 저장 (UI 출력용)
                base_percent = base_rate * 100
                miracle_percent = base_percent * 2
                prob_info_text.append(f"- **{route}** : 1회 시도 기본 **{base_percent:.4f}%** (미라클 타임 **{miracle_percent:.4f}%**)")
                    
                actual_rate = base_rate * 2 if miracle_time else base_rate
                
                avg_tries = int(1 / actual_rate)
                max_ceil = ceilings.get(route, 999)
                
                actual_tries = min(avg_tries, max_ceil)
                total_tries += actual_tries
                total_cost_val += actual_tries * costs[grades[i]]
                
                if max_ceil != 999:
                    ceil_cost = max_ceil * costs[grades[i]]
                    ceil_info_text.append(f"📌 {route} 확정 천장: {max_ceil}회 (비용: 약 {ceil_cost / 100000000:.2f}억 메소)")

            st.markdown("---")
            st.subheader(f"📊 {item_level_cube}제 장비 등업 리포트")
            
            # 구간별 1회 시도 확률 출력
            st.markdown("#### 🎲 선택하신 구간의 확률 정보")
            for p_text in prob_info_text:
                st.write(p_text)
            st.markdown("<br>", unsafe_allow_html=True)
            
            c1, c2, c3 = st.columns(3)
            c1.metric("🔮 누적 기대 시도 횟수", f"{total_tries:,} 회")
            
            if is_meso_system:
                c2.metric("💰 평균 기대 비용", f"{int(total_cost_val / 100000000):,}억 메소")
                c3.metric("🪙 정확한 메소 수치", f"{total_cost_val:,} 메소")
            else:
                c2.metric("🎟️ 필요 큐브 기댓값", f"{total_tries:,} 개")

            # 천장 시스템 UI 출력 (배경색 없이 글자만 굵고 크게 표기)
            if ceil_info_text:
                st.markdown("<br>", unsafe_allow_html=True)
                for t in ceil_info_text:
                    st.markdown(f"<p style='font-size: 26px; font-weight: 900; color: #ff4b4b; margin: 5px 0;'>{t}</p>", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)


# ==========================================
# 2. 잠재능력 옵션 저격 시뮬레이터 탭
# ==========================================
with tab2:
    st.header("🎯 잠재능력 커스텀 수치(%) 옵션 저격")
    st.caption("원하는 옵션과 수치(%)를 직접 설정해 이탈(프라임) 옵션 확률까지 고려하여 기댓값을 산출합니다.")
    
    co1, co2 = st.columns(2)
    with co1:
        item_level_opt = st.selectbox("장비 레벨 (옵션 저격용)", [140, 150, 160, 200, 250], index=3, key="opt_lvl")
        cube_type_opt = st.selectbox("사용 시스템", ["잠재능력 재설정 (메소 소모)", "에디셔널 재설정 (메소 소모)"])
    with co2:
        target_grade_opt = st.selectbox("장비 등급", ["레전더리", "유니크"])
        item_cat = st.selectbox("장비 부위", ["무기/보조무기/엠블렘", "장갑", "기타 방어구/장신구"])

    st.markdown("### 🎯 목표 옵션 상세 설정 (수치 입력)")
    st.write("※ **프라임(이탈) 옵션 판정:** 레전더리 기준 주스탯 12%, 크뎀 8%, 보공 40% 이상 등 기입 시 난이도가 기하급수적으로 상승합니다.")
    
    c_opt1, c_opt2, c_opt3 = st.columns(3)
    with c_opt1:
        o1_type = st.selectbox("1번째 줄", ["상관없음", "공격력/마력", "보스 몬스터 공격 시 데미지", "방어율 무시", "크리티컬 데미지", "주스탯", "올스탯", "아이템 드롭률", "메소 획득량"])
        o1_val = st.number_input("1번째 줄 (%)", min_value=0, max_value=40, step=1, value=12)
    with c_opt2:
        o2_type = st.selectbox("2번째 줄", ["상관없음", "공격력/마력", "보스 몬스터 공격 시 데미지", "방어율 무시", "크리티컬 데미지", "주스탯", "올스탯", "아이템 드롭률", "메소 획득량"])
        o2_val = st.number_input("2번째 줄 (%)", min_value=0, max_value=40, step=1, value=9)
    with c_opt3:
        o3_type = st.selectbox("3번째 줄", ["상관없음", "공격력/마력", "보스 몬스터 공격 시 데미지", "방어율 무시", "크리티컬 데미지", "주스탯", "올스탯", "아이템 드롭률", "메소 획득량"])
        o3_val = st.number_input("3번째 줄 (%)", min_value=0, max_value=40, step=1, value=9)

    if st.button("🎯 옵션 저격 기댓값 계산"):
        def is_prime(o_type, o_val):
            if o_type == "크리티컬 데미지" and o_val >= 8: return True
            if o_type in ["공격력/마력", "주스탯"] and o_val >= 12: return True
            if o_type in ["보스 몬스터 공격 시 데미지", "방어율 무시"] and o_val >= 40: return True
            if o_type in ["올스탯", "아이템 드롭률", "메소 획득량"] and o_val >= 20: return True
            return False

        lines = [(o1_type, o1_val), (o2_type, o2_val), (o3_type, o3_val)]
        wanted_lines = [l for l in lines if l[0] != "상관없음"]
        prime_count = sum(1 for l in wanted_lines if is_prime(l[0], l[1]))
        
        if not wanted_lines:
            st.warning("목표 옵션을 최소 1개 이상 지정해주세요.")
        else:
            base_tries = 1
            for l in wanted_lines:
                base_tries *= 14  
            
            if prime_count > 1:
                base_tries *= (10 ** (prime_count - 1))
                
            if item_cat == "장갑" and any(l[0] == "크리티컬 데미지" for l in wanted_lines): base_tries *= 2
            if item_cat == "무기/보조무기/엠블렘" and any(l[0] == "보스 몬스터 공격 시 데미지" for l in wanted_lines): base_tries *= 3

            level_scale = {140: 0.45, 150: 0.60, 160: 0.70, 200: 1.0, 250: 1.25}
            scale = level_scale[item_level_opt]
            cost_per_try = int(45000000 * scale) if "잠재능력" in cube_type_opt else int(88000000 * scale)
            
            expected_cost = int(base_tries * cost_per_try)

            st.markdown("---")
            st.subheader(f"📊 {item_level_opt}제 {target_grade_opt} 옵션 저격 리포트")
            st.info(f"💡 분석 결과: **프라임(이탈) 옵션 요구 개수 {prime_count}개**가 포함된 구성입니다.")
            
            r1, r2 = st.columns(2)
            r1.metric("🔮 옵션 저격 기대 시도 횟수", f"{int(base_tries):,} 회")
            r2.metric("💰 평균 기대 비용", f"{int(expected_cost / 100000000):,}억 메소")


# ==========================================
# 3. 스타포스 시뮬레이터 탭 (2026 룰 적용)
# ==========================================
with tab3:
    st.header("⭐ 정밀 스타포스 계산기 (2026 최신 룰)")
    st.caption("스타캐치 상시 적용 및 아이템 파괴 시 파괴 직전 흔적으로 보존되는 **'신규 복구 시스템'**이 적용되었습니다.")

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        item_level = st.selectbox("장비 레벨 제한 선택", [140, 150, 160, 200, 250], index=3, key="sf_lvl")
        curr_star = st.slider("현재 스타포스", 0, 24, 15)
        target_star = st.slider("목표 스타포스", 1, 25, 22)
    
    with col_s2:
        st.write("⚙️ 인게임 조건 세부 설정")
        event_type = st.selectbox("선데이 메이플 이벤트", [
            "이벤트 없음", 
            "샤이닝 스타포스 (30% 할인 + 5/10/15성 100%)", 
            "스타포스 30% 할인", 
            "5/10/15성 성공확률 100%", 
            "10성 이하 1+1 강화"
        ])
        prevent_15_17 = st.checkbox("15성~17성 파괴방지 (메소 비용 100% 가산)")
        
        st.markdown("**🔄 파괴 흔적 복구 설정**")
        restore_cost = st.number_input("파괴 1회당 총 복구 비용 (억 메소)", min_value=0.0, max_value=1000.0, value=25.0, step=1.0)
        st.caption("스페어 장비 가격 + 메소 복구 비용을 합산하여 적어주세요. (파괴 시 강화 단계는 하락하지 않습니다)")

    if st.button("⭐ 스타포스 1,000회 시뮬레이션 가동"):
        if curr_star >= target_star:
            st.error("❌ 목표 성급이 현재 성급보다 높아야 계산할 수 있습니다.")
        else:
            sim_counts = 1000
            results_meso = []
            results_destroy = []

            with st.spinner("🚀 1,000번의 강화 가챠 시뮬레이션을 돌리는 중..."):
                for _ in range(sim_counts):
                    star = curr_star
                    total_meso = 0
                    destroy_count = 0
                    chance_time = False
                    fail_streak = 0

                    while star < target_star:
                        if star < 10:
                            cost = 1000 + (item_level**3) * (star + 1) / 2500
                        elif star < 15:
                            cost = 1000 + (item_level**3) * ((star + 1)**2.7) / 400
                        else:
                            cost = 1000 + (item_level**3) * ((star + 1)**2.7) / 200

                        if prevent_15_17 and star in [15, 16, 17]:
                            cost *= 2
                        if "30% 할인" in event_type or "샤이닝" in event_type:
                            cost *= 0.7
                        
                        total_meso += cost

                        if chance_time:
                            star += 1
                            chance_time = False
                            fail_streak = 0
                            continue

                        success_rates = {12: 0.40, 13: 0.35, 14: 0.30, 15: 0.30, 16: 0.30, 17: 0.30, 18: 0.30, 19: 0.30, 20: 0.10, 21: 0.10, 22: 0.03}
                        destroy_rates = {15: 0.021, 16: 0.021, 17: 0.021, 18: 0.028, 19: 0.028, 20: 0.10, 21: 0.10, 22: 0.194}

                        s_rate = success_rates.get(star, 0.50 if star < 12 else 0.01)
                        d_rate = destroy_rates.get(star, 0.0)

                        s_rate *= 1.05

                        if ("100%" in event_type or "샤이닝" in event_type) and star in [5, 10, 15]:
                            s_rate = 1.0

                        rand_val = random.random()

                        if rand_val < s_rate:
                            if "1+1" in event_type and star <= 10:
                                star += 2
                            else:
                                star += 1
                            fail_streak = 0
                        
                        elif rand_val < (s_rate + d_rate) and not (prevent_15_17 and star in [15, 16, 17]):
                            destroy_count += 1
                            total_meso += (restore_cost * 100000000) 
                            fail_streak = 0
                            
                        else:
                            if star in [15, 20]:
                                pass
                            elif star > 10:
                                star -= 1
                                fail_streak += 1
                                if fail_streak >= 2:
                                    chance_time = True
                    
                    results_meso.append(total_meso)
                    results_destroy.append(destroy_count)

            avg_meso = sum(results_meso) / sim_counts
            avg_destroy = sum(results_destroy) / sim_counts

            st.markdown("---")
            st.subheader(f"📊 {item_level}제 장비 스타포스 결과 (2026년 룰, 1000회 통계)")
            
            c1, c2, c3 = st.columns(3)
            c1.metric("💰 평균 소모 메소 (복구비 포함)", f"{int(avg_meso / 100000000):,}억 메소")
            c2.metric("💥 평균 파괴 횟수", f"{avg_destroy:.2f}회 파괴")
            c3.metric("⏱️ 기대 시도 횟수", f"{int(avg_meso / 12000000):,}번 클릭")
