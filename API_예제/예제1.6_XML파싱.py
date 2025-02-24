import requests
import xml.etree.ElementTree as ET

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
    "returnType": "XML",  # ✅ XML 형식으로 응답 요청
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

if response.status_code == 200:
    print("\n📌 응답 받은 XML 데이터:\n")
    print(response.text)  # XML 원본 출력

    try:
        # XML 파싱
        root = ET.fromstring(response.text)

        # 검색된 데이터 개수 확인
        result_count = root.find("scn_cnt").text if root.find("scn_cnt") is not None else "0"

        if result_count == "0":
            print("\n🔍 검색된 훈련 과정이 없습니다.")
        else:
            print("\n✅ 훈련 과정 목록:")
            
            # <scn_list> 태그에서 훈련 과정 정보 추출
            for idx, training in enumerate(root.findall(".//scn_list"), start=1):
                title = training.find("title").text if training.find("title") is not None else "N/A"
                tra_start_date = training.find("traStartDate").text if training.find("traStartDate") is not None else "N/A"
                tra_end_date = training.find("traEndDate").text if training.find("traEndDate") is not None else "N/A"
                training_hours = training.find("trngHour").text if training.find("trngHour") is not None else "N/A"

                print(f"\n🔹 [{idx}] 과정명: {title}")
                print(f"   시작일: {tra_start_date}")
                print(f"   종료일: {tra_end_date}")
                print(f"   훈련시간: {training_hours}시간")

    except ET.ParseError:
        print("❌ XML 파싱 오류 발생! 응답이 XML 형식이 아닙니다.")

else:
    print(f"❌ 오류 발생: {response.status_code}")
    print("응답 내용:", response.text)  # 오류 메시지 확인
