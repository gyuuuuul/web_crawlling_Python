import requests

# API 키 설정
authKey = "9f166e67-b76e-49f2-a34b-5e93e71e3cf6"

# 요청 URL
REQUEST_URL = "https://www.work24.go.kr/cm/openApi/call/hr/callOpenApiSvcInfo310L01.do"

# 사용자 입력 받기
training_organization = input("검색할 훈련기관명을 입력하세요: ")
start_date = input("검색할 훈련 시작일을 입력하세요 (예: 20250101): ")
end_date = input("검색할 훈련 종료일을 입력하세요 (예: 20251231): ")

# 요청 파라미터 설정
params = {
    "authKey": authKey,
    "returnType": "JSON",  # ✅ JSON 형식으로 응답 요청
    "outType": "1",
    "pageNum": "1",
    "pageSize": "10",
    "srchTraOrganNm": training_organization,
    "srchTraStDt": start_date,
    "srchTraEndDt": end_date,
    "sort": "ASC",
    "sortCol": "TRNG_BGDE"
}

# API 요청 보내기
response = requests.get(REQUEST_URL, params=params)

# 응답 상태 코드 확인
print(f"응답 코드: {response.status_code}")

# JSON 응답 처리
if response.status_code == 200:
    try:
        # JSON 원본 출력
        print("\n📌 응답 받은 JSON 데이터 (파싱 전):\n")
        print(response.text)
        
        # JSON 데이터 파싱 (문자열 → Python 객체 변환)
        json_data = response.json()

        # ✅ 훈련 과정 목록이 있는지 확인
        if "srchList" in json_data and json_data["srchList"]:
            print("\n✅ 훈련 과정 목록:")

            for idx, training in enumerate(json_data["srchList"], start=1):
                title = training.get("title", "N/A")
                tra_start_date = training.get("traStartDate", "N/A")
                tra_end_date = training.get("traEndDate", "N/A")
                training_hours = training.get("trngHour", "N/A")

                print(f"\n🔹 [{idx}] 과정명: {title}")
                print(f"   시작일: {tra_start_date}")
                print(f"   종료일: {tra_end_date}")
                print(f"   훈련시간: {training_hours}시간")

        else:
            print("\n🔍 검색된 훈련 과정이 없습니다.")

    except requests.exceptions.JSONDecodeError:
        print("❌ JSON 변환 오류! 응답이 JSON 형식이 아닙니다.")
        print("응답 내용:", response.text)  # 원본 응답 확인

else:
    print(f"❌ 오류 발생: {response.status_code}")
    print("응답 내용:", response.text)  # 오류 메시지 확인
