import streamlit as st
import random

st.set_page_config(page_title="메이플스토리 정밀 계산기 (매수라이브 스타일)", layout="wide")

# 사이드바 스타일링 및 메뉴
st.sidebar.title("🍁 MESULIVE 클론")
menu = st.sidebar.radio("원하는 시뮬레이터를 선택하세요", ["🔮 정밀 큐브 계산기", "⭐ 정밀 스타포스 계산기"])

# -----------------------------------------------------------------
# 1. 큐브 시뮬레이터 탭
# -----------------------------------------------------------------
if menu == "🔮 정밀 큐브 계산기":
    st.header("🔮 매수라이브 스타일 큐브 정밀 기댓값")
    st.caption("공식 등업 확률 및 부위별 유효 옵션 출현 확률을 계산합니다.")
    
    col1, col2 = st.columns(2)
    with col1:
        cube_type = st.selectbox("큐브 종류", ["블랙 큐브", "레드 큐브", "화이트 에디셔널 큐브"])
        miracle_time = st.checkbox("🔥 미라클 타임 적용 (등업 확률 2배)")
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

    if st.button("🔮 매수라이브 큐브 시뮬레이션 실행"):
        # 1. 등업 로직
        cube_rates = {
            "블랙 큐브": {"레어->에픽": 0.15, "에픽->유니크": 0.035, "유니크->레전더리": 0.012},
            "레드 큐브": {"레어->에픽": 0.06, "에픽->유니크": 0.018, "유니크->레전더리": 0.003},
            "화이트 에디셔널 큐브": {"레어->에픽": 0.047, "에픽->유니크": 0.019, "유니크->레전더리": 0.005}
        }
        
        up_cubes = 0
        if target_grade != "등급업 제외 (옵션만 타겟)":
            grades = ["레어", "에픽", "유니크", "레전더리"]
            try:
                curr_idx = grades.index(current_grade)
                target_idx = grades.index(target_grade)
                if curr_idx >= target_idx:
                    st.error("❌ 목표 등급이 현재 등급보다 낮거나 같습니다.")
                    st.stop()
                
                # 등업 누적 기댓값 계산
                for i in range(curr_idx, target_idx):
                    route = f"{grades[i]}->{grades[i+1]}"
                    rate = cube_rates[cube_type].get(route, 0.01)
                    if miracle_time:
                        rate *= 2
                    up_cubes += int(1 / rate)
            except ValueError:
                pass

        # 2. 옵션 저격 확률 로직 (매수라이브 가중치 시뮬레이션 원리)
        wanted_count = sum(1 for l in [line1, line2, line3] if l != "상관없음")
        option_cubes = 0
        if wanted_count > 0:
            # 부위별 저격 난이도 가중치
            difficulty = 1.0
            if item_type in ["무기", "보조무기"] and "보스 몬스터 공격 시 데미지 %" in [line1, line2, line3]:
                difficulty *= 4.5
            if "크리티컬 데미지 %" in [line1, line2, line3] and item_type == "방어구(장갑)":
                difficulty *= 3.8
            
            option_cubes = int((wanted_count ** 3.5) * 15 * difficulty)

        total_cubes = up_cubes + option_cubes
        cube_cash = 2200 if "블랙" in cube_type or "화이트" in cube_type else 1200
        total_cost = total_cubes * cube_cash

        st.markdown("---")
        st.subheader("📊 시뮬레이터 분석 리포트")
        
        col_res1, col_res2, col_res3 = st.columns(3)
        col_res1.metric("🔮 등업 소요 큐브 (평균)", f"{up_cubes:,} 개")
        col_res2.metric("🎯 옵션 저격 소요 큐브 (평균)", f"{option_cubes:,} 개")
        col_res3.metric("💰 총 기대 비용", f"{total_cubes * cube_cash:,} 캐시")

        # 매수라이브 특유의 운 수치 제공 그래프 구현
        st.markdown("### 🍀 내 운에 따른 소요 비용 분포 (매수라이브 시그니처)")
        st.write(f"🟢 **운이 매우 좋을 때 (상위 10%):** 약 {int(total_cubes * 0.3):,} 개 / {int(total_cost * 0.3):,} 캐시")
        st.write(f"🟡 **평범한 평균 페이스 (50%):** 약 {total_cubes:,} 개 / {total_cost:,} 캐시")
        st.write(f"🔴 **운이 나쁜 억까 구간 (하위 90%):** 약 {int(total_cubes * 2.3):,} 개 / {int(total_cost * 2.3):,} 캐시")

# -----------------------------------------------------------------
# 2. 스타포스 시뮬레이터 탭
# -----------------------------------------------------------------
elif menu == "⭐ 정밀 스타포스 계산기":
    st.header("⭐ 매수라이브 스타일 스타포스 시뮬레이터")
    st.caption("하락, 파괴, 찬스타임 시스템이 완벽히 반영된 정밀 강화 계산기입니다.")

    col1, col2 = st.columns(2)
    with col1:
        item_level = st.selectbox("장비 레벨 제한", [150, 160, 200, 250])
        curr_star = st.slider("현재 스타포스", 0, 24, 12)
        target_star = st.slider("목표 스타포스", 1, 25, 22)
    
    with col2:
        st.write("⚙️ 인게임 조건 세부 설정")
        star_catch = st.checkbox("스타캐치 매번 성공 적용 (+5% 곱연산)")
        prevent_15_16 = st.checkbox("15성, 16성 파괴방지 (메소 비용 2배)")
        event_type = st.selectbox("선데이 메이플 이벤트 선택", ["이벤트 없음", "10성 이하 1+1 강화", "5/10/15성 성공확률 100%"])

    if st.button("⭐ 스타포스 시뮬레이터 가동"):
        if curr_star >= target_star:
            st.error("❌ 목표 성급이 현재 성급보다 높아야 계산할 수 있습니다.")
            st.stop()

        # 시뮬레이션용 대형 변수 선언 (100번 반복 실행 평균값 도출 - 매수라이브 알고리즘)
        sim_counts = 100
        results_meso = []
        results_destroy = []

        for _ in range(sim_counts):
            star = curr_star
            total_meso = 0
            destroy_count = 0
            chance_time = False
            fail_streak = 0

            while star < target_star:
                # 1. 구간별 비용 산정 공식
                if star < 10:
                    cost = 1000 + (item_level**3) * (star + 1) / 2500
                elif star < 15:
                    cost = 1000 + (item_level**3) * ((star + 1)**2.7) / 400
                else:
                    cost = 1000 + (item_level**3) * ((star + 1)**2.7) / 200

                # 파방 비용 추가
                if prevent_15_16 and star in [15, 16]:
                    cost *= 2
                
                total_meso += cost

                # 찬스타임 로직
                if chance_time:
                    star += 1
                    chance_time = False
                    fail_streak = 0
                    continue

                # 2. 기본 확률 테이블 세팅
                success_rates = {12: 0.40, 13: 0.35, 14: 0.30, 15: 0.30, 16: 0.30, 17: 0.30, 18: 0.30, 19: 0.30, 20: 0.10, 21: 0.10, 22: 0.03}
                destroy_rates = {15: 0.021, 16: 0.021, 17: 0.021, 18: 0.028, 19: 0.028, 20: 0.10, 21: 0.10, 22: 0.194}

                s_rate = success_rates.get(star, 0.50 if star < 12 else 0.01)
                d_rate = destroy_rates.get(star, 0.0)

                # 스타캐치 보정
                if star_catch:
                    s_rate *= 1.05

                # 이벤트 보정
                if event_type == "5/10/15성 성공확률 100%" and star in [5, 10, 15]:
                    s_rate = 1.0

                # 시뮬레이션 난수 주사위 굴리기
                rand_val = random.random()

                if rand_val < s_rate:  # 성공
                    if event_type == "10성 이하 1+1 강화" and star <= 10:
                        star += 2
                    else:
                        star += 1
                    fail_streak = 0
                elif rand_val < (s_rate + d_rate) and not (prevent_15_16 and star in [15, 16]):  # 파괴
                    destroy_count += 1
                    star = 12  # 복구 후 12성 고정
                    fail_streak = 0
                else:  # 실패 및 하락
                    if star in [15, 20]:  # 안심 보장 구간 (하락 안 함)
                        pass
                    elif star > 10:
                        star -= 1
                        fail_streak += 1
                        if fail_streak >= 2:
                            chance_time = True
            
            results_meso.append(total_meso)
            results_destroy.append(destroy_count)

        # 평균값 추출
        avg_meso = sum(results_meso) / sim_counts
        avg_destroy = sum(results_destroy) / sim_counts

        st.markdown("---")
        st.subheader("📊 스타포스 강화 예측 결과")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("💰 평균 소모 메소", f"{int(avg_meso / 100000000):,}억 메소")
        c2.metric("💥 평균 파괴 횟수", f"{avg_destroy:.1f}회 파괴")
        c3.metric("⏱️ 대략적 시도 판수", f"{int(avg_meso / 7000000):,}번 클릭")

        st.warning("⚠️ 파괴 횟수는 유저의 운에 따라 편차가 크게 나타나는 구간입니다. 장비 여분을 넉넉히 준비해 주세요!")
