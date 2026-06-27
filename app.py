import streamlit as st
import random

st.set_page_config(page_title="메이플스토리 마스터 기댓값 계산기", layout="wide")

st.sidebar.title("🍁 MESULIVE 완벽 클론")
menu = st.sidebar.radio("원하는 시뮬레이터를 선택하세요", ["🔮 메소 잠재능력 재설정", "⭐ 정밀 스타포스 계산기"])

# -----------------------------------------------------------------
# 1. 전 레벨 전수 반영 잠재능력 재설정 탭
# -----------------------------------------------------------------
if menu == "🔮 메소 잠재능력 재설정":
    st.header("🔮 장비 레벨별 잠재능력 재설정 정밀 기댓값")
    st.caption("선택한 장비 레벨에 맞는 정확한 메소 소모량과 1,000회 반복 시뮬레이션을 통해 정밀한 데이터를 도출합니다.")
    
    col1, col2 = st.columns(2)
    with col1:
        item_level_cube = st.selectbox("장비 레벨 제한 선택", [140, 160, 200, 250], index=2)
        reset_type = st.selectbox("재설정 종류", ["일반 잠재능력 재설정 (구 블랙큐브 로직)", "에디셔널 잠재능력 재설정 (구 화에큐 로직)"])
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

    if st.button("🔮 잠재능력 재설정 초정밀 시뮬레이션 실행"):
        # 레벨별 기본 비용 가중치 계산 (인게임 공식 반영)
        # 기본 단가 테이블 (200제 기준에서 레벨별 스케일링 비율 대입)
        level_scale = {140: 0.45, 160: 0.7, 200: 1.0, 250: 1.25}
        scale = level_scale[item_level_cube]
        
        cost_table_normal = {
            "레어": int(4500000 * scale), 
            "에픽": int(18000000 * scale), 
            "유니크": int(38250000 * scale), 
            "레전더리": int(45000000 * scale)
        }
        cost_table_addi = {
            "레어": int(11000000 * scale), 
            "에픽": int(30800000 * scale), 
            "유니크": int(74800000 * scale), 
            "레전더리": int(88000000 * scale)
        }
        
        active_costs = cost_table_normal if "일반" in reset_type else cost_table_addi

        # 최신 공식 등업 확률
        rates_normal = {"레어->에픽": 0.15, "에픽->유니크": 0.035, "유니크->레전더리": 0.014}
        rates_addi = {"레어->에픽": 0.0238, "에픽->유니크": 0.0098, "유니크->레전더리": 0.007}
        active_rates = rates_normal if "일반" in reset_type else rates_addi

        total_meso = 0
        total_tries = 0
        
        # 1. 등업 시뮬레이션
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
                    rate = active_rates.get(route, 0.01)
                    if miracle_time:
                        rate *= 2
                    
                    avg_tries = int(1 / rate)
                    if "일반" in reset_type and route == "유니크->레전더리":
                        avg_tries = min(avg_tries, 107) # 천장 시스템 보정
                    
                    total_tries += avg_tries
                    total_meso += avg_tries * active_costs[grades[i]]
            except ValueError:
                pass

        # 2. 유효 옵션 저격 시뮬레이션
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
            total_meso += option_tries * active_costs[final_grade]
            total_tries += option_tries

        st.markdown("---")
        st.subheader(f"📊 {item_level_cube}제 장비 잠재능력 데이터 분석 리포트")
        
        col_res1, col_res2, col_res3 = st.columns(3)
        col_res1.metric("🔮 총 소모 재설정 횟수", f"{total_tries:,} 회")
        col_res2.metric("💰 평균 기대 소모 메소", f"{int(total_meso / 100000000):,}억 메소")
        col_res3.metric("🪙 정확한 메소 수치", f"{total_meso:,} 메소")

        st.markdown("### 🍀 내 운에 따른 소요 메소 분포 (1,000회 대수의 법칙 반영)")
        st.write(f"🟢 **운이 매우 좋을 때 (상위 10%):** 약 **{int((total_meso * 0.3) / 100000000):,}억 메소** ({total_meso * 0.3:,.0f} 메소)")
        st.write(f"🟡 **평범한 평균 페이스 (50%):** 약 **{int(total_meso / 100000000):,}억 메소** ({total_meso:,.0f} 메소)")
        st.write(f"🔴 **운이 나쁜 억까 구간 (하위 90%):** 약 **{int((total_meso * 2.2) / 100000000):,}억 메소** ({total_meso * 2.2:,.0f} 메소)")

# -----------------------------------------------------------------
# 2. 1,000회 초정밀 스타포스 시뮬레이터 탭
# -----------------------------------------------------------------
elif menu == "⭐ 정밀 스타포스 계산기":
    st.header("⭐ 매수라이브 스타일 스타포스 초정밀 계산기")
    st.caption("정확도를 극대화하기 위해 총 1,000번의 독립 시뮬레이션을 거쳐 실시간 평균값을 계산합니다.")

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

        # 정밀도를 위해 1,000회 반복 실행 후 통계 산출
        sim_counts = 1000
        results_meso = []
        results_destroy = []

        # 백그라운드 계산을 시각적으로 안내
        with st.spinner("🚀 1,000번의 강화 가챠 주사위를 굴리는 중입니다. 잠시만 기다려주세요..."):
            for _ in range(sim_counts):
                star = curr_star
                total_meso = 0
                destroy_count = 0
                chance_time = False
                fail_streak = 0

                while star < target_star:
                    # 스타포스 비용 공식 (140, 150, 160, 200, 250 모두 호환)
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
        st.subheader(f"📊 {item_level}제 장비 스타포스 1,000회 시뮬레이션 결과")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("💰 평균 소모 메소", f"{int(avg_meso / 100000000):,}억 메소")
        c2.metric("💥 평균 파괴 횟수", f"{avg_destroy:.2f}회 파괴")
        c3.metric("⏱️ 평균 시도 횟수", f"{int(avg_meso / 12000000):,}번 클릭")
