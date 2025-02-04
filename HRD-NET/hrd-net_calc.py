import requests
import time
import pandas as pd
import os

# 바탕화면 경로 설정 (Windows 기준)
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# ✅ 각각의 API 키 설정
Auth_Key_Consortium = "c0885044-4b39-4e48-a19b-2c6fa75f9883"  # 국가인적자원개발 컨소시엄
Auth_Key_Training_Card = "9f166e67-b76e-49f2-a34b-5e93e71e3cf6"  # 국민내일배움카드
Auth_Key_Work_Edu = "639ba02e-e71d-4ba9-a3f9-9838c0ab6eb5"  # 일학습병행 
Auth_Key_Owner = "96a61e6c-bd1f-42c7-9e12-6722d6596162"  # 사업주훈련 

# ✅ 각각의 요청 URL 설정
REQUEST_URL_CONSORTIUM = "https://www.work24.go.kr/cm/openApi/call/hr/callOpenApiSvcInfo312L01.do"
REQUEST_URL_TRAINING_CARD = "https://www.work24.go.kr/cm/openApi/call/hr/callOpenApiSvcInfo310L01.do"
REQUEST_URL_Work_Edu = "https://www.work24.go.kr/cm/openApi/call/hr/callOpenApiSvcInfo313L01.do"
REQUEST_URL_Owner = "https://www.work24.go.kr/cm/openApi/call/hr/callOpenApiSvcInfo311L01.do"

# 사용자 입력 받기
training_organization = input("검색할 훈련기관명을 입력하세요: ")
start_date = input("검색할 훈련 시작일을 입력하세요 (예: 20230101): ")
end_date = input("검색할 훈련 종료일을 입력하세요 (예: 20231231): ")

# 한 페이지당 출력 개수 설정
page_size = 50

# ✅ API 요청 및 데이터 수집 함수
def fetch_training_data(auth_key, request_url, category_name):
    results = []
    page_num = 1
    while True:
        params = {
            "authKey": auth_key,            
            "returnType": "JSON",            
            "outType": "1",                  
            "pageNum": str(page_num),        
            "pageSize": str(page_size),      
            "srchTraOrganNm": training_organization,  
            "srchTraStDt": start_date,  
            "srchTraEndDt": end_date,  
            "sort": "ASC",                   
            "sortCol": "TRNG_BGDE"      
        }

        response = requests.get(request_url, params=params)

        if response.status_code != 200:
            print(f"❌ {category_name} API 오류 발생: {response.status_code}")
            print("응답 내용:", response.text)
            break  

        try:
            data = response.json()
        except requests.exceptions.JSONDecodeError:
            print(f"⚠️ {category_name} JSON 디코딩 오류 발생! 응답이 JSON 형식이 아닙니다.")
            print("응답 내용:", response.text)
            break

        if "srchList" not in data or not data["srchList"]:
            print(f"⚠️ {category_name}: 더 이상 검색된 훈련 과정이 없습니다.")
            break

        for training in data["srchList"]:
            reg_course_man = int(training.get("regCourseMan", 0) or 0)  # 수강 신청 인원
            real_man = int(training.get("realMan", 0) or 0)  # 실제 수강비

            # ✅ 매출액 계산 (수강 신청 인원 * 실제 수강비)
            revenue = reg_course_man * real_man  

            # ✅ 훈련 종료 연도 추출
            tra_end_date = training.get("traEndDate", "N/A")
            tra_end_year = tra_end_date[:4] if tra_end_date != "N/A" else "N/A"  

            results.append({
                "카테고리": category_name,
                "훈련기관 코드": training.get("instCd", "N/A"),
                "과정명": training.get("title", "N/A"),
                "NCS 코드": training.get("ncsCd", "N/A"),
                "훈련 구분": training.get("trainTargetCd", "N/A"),
                "훈련 과정 ID": training.get("trprId", "N/A"),
                "훈련 대상": training.get("trainTarget", "N/A"),
                "훈련 과정 순차": training.get("trprDegr", "N/A"),
                "정원": training.get("yardMan", "N/A"),
                "수강 신청 인원": reg_course_man,
                "수강비": training.get("courseMan", "N/A"),
                "실제 수강비": real_man,
                "매출액": revenue,  # ✅ 추가된 매출액
                "훈련 시작일자": training.get("traStartDate", "N/A"),
                "훈련 종료일자": tra_end_date,
                "훈련 종료 연도": tra_end_year,  # ✅ 훈련 종료 연도 추가
                "훈련시간": training.get("trngHour", training.get("trainingHours", "N/A")),
            })

        page_num += 1
        print(f"✅ {category_name}: {page_num - 1} 페이지 완료, 다음 페이지 요청 중...")
        time.sleep(1)  

    return results

# ✅ 네 개의 API 호출 실행
print("\n📡 국가인적자원개발 컨소시엄 데이터 요청 중...")
results_consortium = fetch_training_data(Auth_Key_Consortium, REQUEST_URL_CONSORTIUM, "국가인적자원개발 컨소시엄")

print("\n📡 국민내일배움카드 데이터 요청 중...")
results_training_card = fetch_training_data(Auth_Key_Training_Card, REQUEST_URL_TRAINING_CARD, "국민내일배움카드")

print("\n📡 일학습병행 과정 데이터 요청 중...")
results_Work_Edu = fetch_training_data(Auth_Key_Work_Edu, REQUEST_URL_Work_Edu, "일학습병행")

print("\n📡 사업주 훈련 과정 데이터 요청 중...")
results_Owner = fetch_training_data(Auth_Key_Owner, REQUEST_URL_Owner, "사업주훈련")

# ✅ 데이터 합치기
final_results = results_consortium + results_training_card + results_Work_Edu + results_Owner

# ✅ 연도별 매출 계산
df = pd.DataFrame(final_results)
yearly_revenue = df.groupby("훈련 종료 연도")["매출액"].sum().reset_index()

# ✅ 엑셀 저장
excel_filename = os.path.join(desktop_path, f"{training_organization}_훈련과정.xlsx")
with pd.ExcelWriter(excel_filename, engine="openpyxl") as writer:
    df.to_excel(writer, sheet_name="훈련 과정 데이터", index=False)
    yearly_revenue.to_excel(writer, sheet_name="연도별 매출", index=False)

print(f"📁 엑셀 파일 저장 완료: {excel_filename}")
