import requests
import time
import pandas as pd
import os  # 바탕화면 경로 설정을 위해 추가

# 바탕화면 경로 설정 (Windows 기준)
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# API 키 설정
Auth_Key = "c0885044-4b39-4e48-a19b-2c6fa75f9883"

# 요청 URL
REQUEST_URL = "https://www.work24.go.kr/cm/openApi/call/hr/callOpenApiSvcInfo312L01.do"

# 사용자 입력 받기
training_organization = input("검색할 훈련기관명을 입력하세요: ")
start_date = input("검색할 훈련 시작일을 입력하세요 (예: 20230101): ")
end_date = input("검색할 훈련 종료일을 입력하세요 (예: 20231231): ")

# 한 페이지당 출력 개수 설정
page_size = 50
results = []

# 페이지를 넘기면서 데이터 가져오기
page_num = 1
while True:
    # 요청 파라미터 설정
    params = {
        "authKey": Auth_Key,            
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

    # API 요청 보내기
    response = requests.get(REQUEST_URL, params=params)
    
    # 응답 상태 코드 확인
    if response.status_code != 200:
        print(f"❌ 오류 발생: {response.status_code}")
        print("응답 내용:", response.text)
        break  

    # JSON 데이터 파싱
    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError:
        print("⚠️ JSON 디코딩 오류 발생! 응답이 JSON 형식이 아닙니다.")
        print("응답 내용:", response.text)
        break

    # 검색된 훈련 과정이 없으면 종료
    if "srchList" not in data or not data["srchList"]:
        print("⚠️ 더 이상 검색된 훈련 과정이 없습니다.")
        break

    # 결과 저장 (훈련시간 + 등급 추가됨)
    for training in data["srchList"]:
        results.append({
            "훈련기관 코드": training.get("instCd", "N/A"),
            "과정명": training.get("title", "N/A"),
            "NCS 코드": training.get("ncsCd", "N/A"),
            "훈련 구분": training.get("trainTargetCd", "N/A"),
            "훈련 과정 ID": training.get("trprId", "N/A"),
            "훈련 대상": training.get("trainTarget", "N/A"),
            "훈련 과정 순차": training.get("trprDegr", "N/A"),
            "정원": training.get("yardMan", "N/A"),
            "수강 신청 인원": training.get("regCourseMan", "N/A"),
            "수강비": training.get("courseMan", "N/A"),
            "실제 수강비": training.get("realMan", "N/A"),
            "훈련 시작일자": training.get("traStartDate", "N/A"),
            "훈련 종료일자": training.get("traEndDate", "N/A"),
            "훈련시간": training.get("trngHour", training.get("trainingHours", "N/A")),
            "등급": training.get("grade", "N/A"),
            "컨텐츠": training.get("contents", "N/A"),
        })

    # 다음 페이지 요청을 위해 증가
    page_num += 1
    print(f"✅ {page_num - 1} 페이지 완료, 다음 페이지 요청 중...")
    
    # 서버 부하 방지를 위해 잠깐 대기
    time.sleep(1)  

# 최종 결과 출력 및 엑셀 저장
if results:
    print("\n📌 검색된 훈련 과정 목록:")
    for idx, result in enumerate(results, start=1):
        print(f"{idx}. 과정명: {result['과정명']}")
        print(f"   훈련기관 코드: {result['훈련기관 코드']}")
        print(f"   NCS 코드: {result['NCS 코드']}")
        print(f"   훈련 구분: {result['훈련 구분']}")
        print(f"   훈련 과정 ID: {result['훈련 과정 ID']}")
        print(f"   훈련 대상: {result['훈련 대상']}")
        print(f"   훈련 과정 순차: {result['훈련 과정 순차']}")
        print(f"   정원: {result['정원']}")
        print(f"   수강 신청 인원: {result['수강 신청 인원']}")
        print(f"   수강비: {result['수강비']}원")
        print(f"   실제 수강비: {result['실제 수강비']}원")
        print(f"   훈련 시작일자: {result['훈련 시작일자']}")
        print(f"   훈련 종료일자: {result['훈련 종료일자']}")
        print(f"   훈련시간: {result['훈련시간']} 시간")
        print(f"   등급: {result['등급']}")
        print(f"   컨텐츠: {result['컨텐츠']}\n")

    # ✅ 바탕화면에 엑셀 저장
    excel_filename = os.path.join(desktop_path, f"{training_organization}_국가인적자원개발컨소시엄_훈련과정.xlsx")
    df = pd.DataFrame(results)
    df.to_excel(excel_filename, index=False, engine="openpyxl")
    
    print(f"📁 엑셀 파일 저장 완료: {excel_filename}")
else:
    print("❌ 검색된 훈련 과정이 없습니다.")
