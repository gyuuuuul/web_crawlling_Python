import requests
import xml.etree.ElementTree as ET

# API 키 설정 (네가 발급받은 키로 변경해야 함)
authKey = "9f166e67-b76e-49f2-a34b-5e93e71e3cf6"


# 요청 URL (고용24 API 실제 URL로 변경 필요)
REQUEST_URL = "https://www.work24.go.kr/cm/openApi/call/hr/callOpenApiSvcInfo310L01.do"

# 사용자 입력 받기
training_organization = input("검색할 훈련기관명을 입력하세요: ")
start_date = input("검색할 훈련 시작일을 입력하세요 (예: 20250101): ")
end_date = input("검색할 훈련 종료일을 입력하세요 (예: 20251231): ")

# 요청 파라미터 설정
params = {
    "authKey": authKey,             # 필수 인증 키
    "returnType": "XML",             # 응답 형식 (XML)
    "outType": "1",                  # '1' = 리스트, '2' = 상세
    "pageNum": "1",                  # 시작 페이지
    "pageSize": "10",                # 페이지당 출력 건수
    "srchTraStDt": start_date,       # 훈련 시작일 (YYYYMMDD)
    "srchTraEndDt": end_date,        # 훈련 종료일 (YYYYMMDD)
    "srchTraOrganNm": training_organization,  # 훈련기관명
    "sort": "ASC",                   # 정렬 방법 (오름차순)
    "sortCol": "TRA_START_DATE"       # 정렬 기준 (훈련 시작일 기준)
}

# API 요청 보내기
response = requests.get(REQUEST_URL, params=params)

# 응답 상태 코드 확인
print(f"응답 코드: {response.status_code}")