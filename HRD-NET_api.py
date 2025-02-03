import requests
import time
import pandas as pd
import os

# 바탕화면 경로 설정
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# ✅ API 키 설정
AUTH_KEYS = {
    "국가인적자원개발 컨소시엄": "c0885044-4b39-4e48-a19b-2c6fa75f9883",
    "국민내일배움카드": "9f166e67-b76e-49f2-a34b-5e93e71e3cf6",
    "일학습병행": "639ba02e-e71d-4ba9-a3f9-9838c0ab6eb5",
    "사업주훈련": "96a61e6c-bd1f-42c7-9e12-6722d6596162"
}

# ✅ 요청 URL 설정
REQUEST_URLS = {
    "국가인적자원개발 컨소시엄": "https://www.work24.go.kr/cm/openApi/call/hr/callOpenApiSvcInfo312L01.do",
    "국민내일배움카드": "https://www.work24.go.kr/cm/openApi/call/hr/callOpenApiSvcInfo310L01.do",
    "일학습병행": "https://www.work24.go.kr/cm/openApi/call/hr/callOpenApiSvcInfo313L01.do",
    "사업주훈련": "https://www.work24.go.kr/cm/openApi/call/hr/callOpenApiSvcInfo311L01.do"
}

# ✅ 상세 정보 요청 URL 설정
DETAIL_URLS = {
    "국가인적자원개발 컨소시엄": "https://www.work24.go.kr/cm/openApi/call/hr/callOpenApiSvcInfo312D01.do",
    "국민내일배움카드": "https://www.work24.go.kr/cm/openApi/call/hr/callOpenApiSvcInfo310L02.do",
    "일학습병행": "https://www.work24.go.kr/cm/openApi/call/hr/callOpenApiSvcInfo313D01.do",
    "사업주훈련": "https://www.work24.go.kr/cm/openApi/call/hr/callOpenApiSvcInfo311D01.do"
}

# 사용자 입력 받기
training_organization = input("검색할 훈련기관명을 입력하세요: ")
start_date = input("검색할 훈련 시작일을 입력하세요 (예: 20230101): ")
end_date = input("검색할 훈련 종료일을 입력하세요 (예: 20231231): ")

# 한 페이지당 출력 개수 설정
page_size = 50

# ✅ 훈련 과정 조회 함수
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
            break

        try:
            data = response.json()
        except requests.exceptions.JSONDecodeError:
            break

        if "srchList" not in data or not data["srchList"]:
            break

        for training in data["srchList"]:
            reg_course_man = int(training.get("regCourseMan", 0) or 0)
            real_man = int(training.get("realMan", 0) or 0)
            revenue = reg_course_man * real_man
            tra_end_date = training.get("traEndDate", "N/A")
            tra_end_year = tra_end_date[:4] if tra_end_date != "N/A" else "N/A"

            results.append({
                "카테고리": category_name,
                "훈련기관 코드": training.get("instCd", "N/A"),
                "과정명": training.get("title", "N/A"),
                "훈련 과정 ID": training.get("trprId", "N/A"),
                "훈련 과정 순차": training.get("trprDegr", "N/A"),
                "정원": training.get("yardMan", "N/A"),
                "수강 신청 인원": reg_course_man,
                "수강비": training.get("courseMan", "N/A"),
                "실제 수강비": real_man,
                "매출액": revenue,
                "훈련 시작일자": training.get("traStartDate", "N/A"),
                "훈련 종료일자": tra_end_date,
                "훈련 종료 연도": tra_end_year,
                "훈련시간": training.get("trngHour", training.get("trainingHours", "N/A")),
                "NCS 코드": "조회 중...",
                "NCS 명": "조회 중...",
                "NCS 여부": "조회 중..."
            })

        page_num += 1
        time.sleep(0.5)

    return results

# ✅ 훈련 과정 상세 정보 조회 함수
def fetch_course_info(training_data, auth_key, category_name):
    """각 훈련 유형에 대한 상세 정보를 조회하여 추가 정보를 포함"""
    results = []
    detail_url = DETAIL_URLS[category_name]

    for course in training_data:
        trpr_id = course["훈련 과정 ID"]
        trpr_degr = course["훈련 과정 순차"]
        inst_cd = course["훈련기관 코드"]

        if not trpr_id or not trpr_degr or not inst_cd:
            course.update({
                "NCS 코드": "N/A",
                "NCS 명": "N/A",
                "NCS 여부": "N/A",
                "정부지원금": "N/A",
                "총 훈련일수": "N/A",
                "총 훈련시간": "N/A",
                "시설 면적(㎡)": "N/A",
                "인원 수(명)": "N/A"
            })
            results.append(course)
            continue

        params = {
            "authKey": auth_key,
            "returnType": "JSON",
            "outType": "2",
            "srchTrprId": trpr_id,
            "srchTrprDegr": trpr_degr,
            "srchTorgId": inst_cd
        }

        response = requests.get(detail_url, params=params)

        if response.status_code == 200:
            try:
                data = response.json()
                course.update({
                    "NCS 코드": data.get("inst_base_info", {}).get("ncsCd", "N/A"),
                    "NCS 명": data.get("inst_base_info", {}).get("ncsNm", "N/A"),
                    "NCS 여부": data.get("inst_base_info", {}).get("ncsYn", "N/A"),
                    "정부지원금": data.get("inst_base_info", {}).get("perTrco", "N/A"),
                    "총 훈련일수": data.get("inst_base_info", {}).get("trDcnt", "N/A"),
                    "총 훈련시간": data.get("inst_detail_info", {}).get("totTraingTime", "N/A"),
                    "시설 면적(㎡)": data.get("inst_facility_detail_info_list", [{}])[0].get("fcltyArCn", "N/A"),
                    "인원 수(명)": data.get("inst_facility_detail_info_list", [{}])[0].get("ocuAcptnNmprCn", "N/A")
                })
            except requests.exceptions.JSONDecodeError:
                pass
        results.append(course)
        time.sleep(0.3)

    return results

# ✅ API 호출 실행
final_results = []
for category, url in REQUEST_URLS.items():
    auth_key = AUTH_KEYS[category]
    results = fetch_training_data(auth_key, url, category)
    detailed_results = fetch_course_info(results, auth_key, category)
    final_results.extend(detailed_results)

# ✅ 엑셀 저장
df = pd.DataFrame(final_results)
excel_filename = os.path.join(desktop_path, f"{training_organization}_훈련과정.xlsx")
df.to_excel(excel_filename, index=False, engine="openpyxl")

print(f"📁 엑셀 파일 저장 완료: {excel_filename}")