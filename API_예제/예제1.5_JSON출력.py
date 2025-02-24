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
    "returnType": "JSON",  # ✅ JSON 형식으로 요청
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

# JSON을 파싱하지 않고 그대로 출력
if response.status_code == 200:
    print("\n📌 응답 받은 JSON 데이터 (파싱하지 않음):\n")
    print(response.text)  # JSON 원본 출력 (문자열 그대로)
else:
    print(f"❌ 오류 발생: {response.status_code}")
    print("응답 내용:", response.text)  # 오류 메시지 확인
