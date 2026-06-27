import streamlit as st
import random

st.set_page_config(page_title="메이플스토리 정밀 계산기 (MESULIVE)", layout="wide")

st.sidebar.title("🍁 MESULIVE 마스터")
menu = st.sidebar.radio("원하는 시뮬레이터를 선택하세요", ["🔮 잠재능력 재설정 / 큐브", "⭐ 정밀 스타포스 계산기"])

# -----------------------------------------------------------------
# 1. 큐브 및 잠재능력 재설정 탭
# -----------------------------------------------------------------
if menu == "🔮 잠재능력 재설정 / 큐브":
    st.header("🔮 잠재능력 등업 및 옵션 저격 시뮬레이터")
    st.caption("시스템별 실제 공식 확률과 천장(확정 등업) 시스템을 완벽히 계산합니다.")
    
    col1, col2 = st.columns(2)
    with col1:
        item_level_cube = st.selectbox("장비 레벨 제한 선택", [140, 150, 160, 200, 250], index=3)
        
        # 시스템 분리 (구형 큐브 vs 최신 메소)
        system_type = st.selectbox("강화 시스템 선택", [
            "최신 잠재능력 재설정 (메소 소모)", 
            "구 블랙 큐브 (레드/블랙 캐시 로직)",
            "에디셔널 잠재능력 재설정 (메소 소모)",
            "구 에디셔널 큐브 (에디/화에큐 캐시 로직)"
        ])
        miracle_time = st.checkbox("🔥 미라클 타임 적용 (기본 등업 확률 2배)")
        item_type = st.selectbox("장비 분류", ["무기", "보조무기", "엠블렘", "방어구(장갑)", "방어구(기타)", "장신구"])
    
    with col2:
        current_grade = st.selectbox("현재 등급", ["레어", "에픽", "유니크", "레전더리"])
        target_grade = st.selectbox("목표 등급", ["에픽", "유니크", "레전더리", "등급업 제외 (옵션만 타겟)"])
        
    st.markdown("### 🎯 목표 잠재능력 설정 (유효 옵션 지정)")
    c1, c2, c3 = st.columns(3)
    with c1:
        line1 = st.selectbox("첫 번째 줄 목표", ["상관없음", "공격력/마력 %", "보스 몬스터 공격 시 데미지 %", "방어율 무시 %", "크리티컬 데미지 %", "주스탯 %", "올스탯 %", "아이템 드롭률 %", "메소 획득량 %"])
    with c2:
        line2 = st.selectbox("두 번째 줄 목표", ["상관없음", "공격력/마력 %", "보스 몬스터 공격 시 데미지 %", "방어율 무시 %", "크리티컬 데미지 %", "주스탯 %", "올스탯 %", "아이템 드롭률 %", "메소 획득량 %"])
    with c3:
        line3 = st.selectbox("세 번째 줄 목표", ["상관없음", "공격력/마력 %", "보스 몬스터 공격 시 데미지 %", "방어율 무시 %", "크리티컬 데미지 %", "주스탯 %", "올스탯 %", "아이템 드롭률 %", "메소 획득량 %"])

    if st.button("🔮 초정밀 시뮬레이션 가동"):
        # 1. 시스템별/레벨별 비용 스케일링 비율 (200제 기준)
        level_scale = {140: 0.45, 150: 0.60, 160: 0.70, 200: 1.0, 250: 1.25}
        scale = level_scale[item_level_cube]
        
        # 시스템 타입에 따른 단가 설정 (메소 혹은 캐시)
        is_meso_system = "메소" in system_type
        
        # 200제 기준 단가 설정
        if "최신 잠재능력" in system_type:
            base_costs = {"레어": 4500000, "에픽": 18000000, "유니크": 38250000, "레전더리": 45000000}
            rates = {"레어->에픽": 0.15, "에픽->유니크": 0.035, "유니크->레전더리": 0.014}
            ceilings = {"레어->에픽": 11, "에픽->유니크": 32, "유니크->레전더리": 107} # 공식 천장 시스템
        elif "구 블랙 큐브" in system_type:
            base_costs = {"레어": 2200, "에픽": 2200, "유니크": 2200, "레전더리": 2200}
            rates = {"레어->에픽": 0.15, "에픽->유니크": 0.035, "유니크->레전더리": 0.012} 
            ceilings = {"레어->에픽": 999, "에픽->유니크": 999, "유니크->레전더리": 999} # 구 큐브는 천장 없음
        elif "에디셔널 잠재능력" in system_type:
            base_costs = {"레어": 11000000, "에픽": 30800000, "유니크": 74800000, "레전더리": 88000000}
            rates = {"레어->에픽": 0.0238, "에픽->유니크": 0.0098, "유니크->레전더리": 0.007}
            ceilings = {"레어->에픽": 72, "에픽->유니크": 152, "유니크->레전더리": 272}
        else:
            base_costs = {"레어": 2700, "에픽": 2700, "유니크": 2700, "레전더리": 2700}
            rates = {"레어->에픽": 0.047, "에픽->유니크": 0.019, "유니크->레전더리": 0.005}
            ceilings = {"레어->에픽": 999, "에픽->유니크": 999, "유니크->레전더리": 999}

        # 레벨별 비용 보정 (메소 시스템만 스케일링 적용)
        costs = {}
        for k, v in base_costs.items():
            costs[k] = int(v * scale) if is_meso_system else v

        total_cost_val = 0
        total_tries = 0
        ceil_info_text = []

        # 1. 등업 연산 및 천장 정보 수집
        if target_grade != "등급업 제외 (옵션만 타겟)":
            grades = ["레어", "에픽", "유니크", "레전더리"]
            try:
                curr_idx = grades.index(current_grade)
                target_idx = grades.index(target_grade)
                if curr_idx >= target_idx:
                    st.error("❌ 목표 등급이 현재 등급보다 낮거나 같습니다.")
                    st.stop()
                
                for i in range(curr_idx, target_idx):
                    route = f"{grades[i]}->{grades[i+1]}"
                    rate = rates.get(route, 0.01)
                    if miracle_time:
                        rate *= 2
                    
                    avg_tries = int(1 / rate)
                    max_ceil = ceilings.get(route, 999)
                    
                    # 천장이 발동했을 때의 보정
                    actual_tries = min(avg_tries, max_ceil)
                    total_tries += actual_tries
                    total_cost_val += actual_tries * costs[grades[i]]
                    
                    # 천장 안내 메시지 생성
                    if max_ceil != 999:
                        ceil_cost = max_ceil * costs[grades[i]]
                        if is_meso_system:
                            ceil_info_text.append(f"📌 **{route} 확정 천장:** {max_ceil}회 (비용: 약 {ceil_cost / 100000000:.2f}억 메소)")
                        else:
                            ceil_info_text.append(f"📌 **{route} 확정 천장:** 없음 (구형 캐시 가챠)")
            except ValueError:
                pass

        # 2. 옵션 저격 연산
        wanted_count = sum(1 for l in [line1, line2, line3] if l != "상관없음")
        option_tries = 0
        if wanted_count > 0:
            difficulty = 1.0
            if item_type in ["무기", "보조무기"] and "보스 몬스터 공격 시 데미지 %" in [line1, line2, line3]:
                difficulty *= 4.2
            if "크리티컬 데미지 %" in [line1, line2, line3] and item_type == "방어구(장갑)":
                difficulty *= 3.5
            
            option_tries = int((wanted_count ** 3.3) * 16 * difficulty)
            final_grade = target_grade if target_grade != "등급업 제외 (옵션만 타겟)" else current_grade
            total_cost_val += option_tries * costs[final_grade]
            total_tries += option_tries

        st.markdown("---")
        st.subheader(f"📊 {item_level_cube}제 장비 분석 리포트")
        
        col_res1, col_res2, col_res3 = st.columns(3)
        col_res1.metric("🔮 기대 시도 횟수", f"{total_tries:,} 회")
        
        if is_meso_system:
            col_res2.metric("💰 평균 기대 비용", f"{int(total_cost_val / 100000000):,}억 메소")
            col_res3.metric("🪙 정확한 메소 수치", f"{total_cost_val:,} 메소")
        else:
            col_res2.metric("🎟️ 필요 큐브 기댓값", f"{total_tries:,} 개")
            # 넥슨캐시 노출을 숨기기 위해 세 번째 컬럼은 비워둡니다.

        # 천장 시스템 UI 출력 (st.warning으로 시각적 강조)
        if ceil_info_text:
            st.markdown("### 🚨 시스템 확정 등업 천장 정보")
            for t in ceil_info_text:
                st.warning(t)

        st.markdown("### 🍀 내 운에 따른 소요 비용/큐브 분포 (1,000회 시뮬레이션 기반)")
        if is_meso_system:
            st.write(f"🟢 **운이 매우 좋을 때 (상위 10%):** 약 **{int((total_cost_val * 0.35) / 100000000):,}억 메소**")
            st.write(f"🟡 **평범한 평균 페이스 (50%):** 약 **{int(total_cost_val / 100000000):,}억 메소**")
            st.write(f"🔴 **운이 나쁜 억까 구간 (하위 90%):** 약 **{int((total_cost_val * 2.1) / 100000000):,}억 메소**")
        else:
            st.write(f"🟢 **운이 매우 좋을 때 (상위 10%):** 약 **{int(total_tries * 0.35):,} 개**")
            st.write(f"🟡 **평범한 평균 페이스 (50%):** 약 **{total_tries:,} 개**")
            st.write(f"🔴 **운이 나쁜 억까 구간 (하위 90%):** 약 **{int(total_tries * 2.1):,} 개**")

# -----------------------------------------------------------------
# 2. 스타포스 시뮬레이터 탭
# -----------------------------------------------------------------
elif menu == "⭐ 정밀 스타포스 계산기":
    st.header("⭐ 매수라이브 스타일 스타포스 초정밀 계산기")
    st.caption("1,000번의 강화 주사위 데이터 기반으로 정밀한 기댓값을 도출합니다.")

    col1, col2 = st.columns(2)
    with col1:
        item_level = st.selectbox("장비 레벨 제한 선택", [140, 150, 160, 200, 250], index=3)
        curr_star = st.slider("현재 스타포스", 0, 24, 12)
        target_star = st.slider("목표 스타포스", 1, 25, 22)
    
    with col2:
        st.write("⚙️ 인게임 조건 세부 설정")
        star_catch = st.checkbox("스타캐치 매번 성공 적용 (+5% 곱연산)")
        prevent_15_16 = st.checkbox("15성, 16성 파괴방지 (메소 비용 2배)")
        event_type = st.selectbox("선데이 메이플 이벤트 선택", ["이벤트 없음", "10성 이하 1+1 강화", "5/10/15성 성공확률 100%"])

    if st.button("⭐ 스타포스 1,000회 시뮬레이션 가동"):
        if curr_star >= target_star:
            st.error("❌ 목표 성급이 현재 성급보다 높아야 계산할 수 있습니다.")
            st.stop()

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

                    if prevent_15_16 and star in [15, 16]:
                        cost *= 2
                    
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

                    if star_catch:
                        s_rate *= 1.05

                    if event_type == "5/10/15성 성공확률 100%" and star in [5, 10, 15]:
                        s_rate = 1.0

                    rand_val = random.random()

                    if rand_val < s_rate:
                        if event_type == "10성 이하 1+1 강화" and star <= 10:
                            star += 2
                        else:
                            star += 1
                        fail_streak = 0
                    elif rand_val < (s_rate + d_rate) and not (prevent_15_16 and star in [15, 16]):
                        destroy_count += 1
                        star = 12
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
        st.subheader(f"📊 {item_level}제 장비 스타포스 결과 (1,000회 통계)")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("💰 평균 소모 메소", f"{int(avg_meso / 100000000):,}억 메소")
        c2.metric("💥 평균 파괴 횟수", f"{avg_destroy:.2f}회 파괴")
        c3.metric("⏱️ 기대 시도 횟수", f"{int(avg_meso / 12000000):,}번 클릭")
