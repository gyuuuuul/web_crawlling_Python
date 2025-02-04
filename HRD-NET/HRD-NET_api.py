import requests
import time
import pandas as pd
import os
import xml.etree.ElementTree as ET  # ✅ XML 파싱을 위한 라이브러리

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
page_size = 100

# ✅ XML 데이터 파싱 함수
def parse_xml(xml_text):
    root = ET.fromstring(xml_text)
    return root

# ✅ 훈련 과정 조회 함수 (XML)
def fetch_training_data(auth_key, request_url, category_name):
    results = []
    page_num = 1
    while True:
        params = {
            "authKey": auth_key,
            "returnType": "XML",  # ✅ XML 응답으로 변경
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
            root = parse_xml(response.text)
        except ET.ParseError:
            break

        scn_list = root.findall(".//scn_list")  # ✅ XML에서 scn_list 요소 찾기
        if not scn_list:
            break

        for training in scn_list:
            results.append({
                "카테고리": category_name,
                "훈련기관 코드": training.findtext("instCd", "N/A"),
                "과정명": training.findtext("title", "N/A"),
                "훈련 과정 ID": training.findtext("trprId", "N/A"),
                "훈련 과정 순차": training.findtext("trprDegr", "N/A"),
                "정원": training.findtext("yardMan", "N/A"),
                "수강 신청 인원": training.findtext("regCourseMan", "0"),
                "수강비": training.findtext("courseMan", "N/A"),
                "실제 수강비": training.findtext("realMan", "N/A"),
                "매출액": int(training.findtext("regCourseMan", "0")) * int(training.findtext("realMan", "0")),
                "훈련 시작일자": training.findtext("traStartDate", "N/A"),
                "훈련 종료일자": training.findtext("traEndDate", "N/A"),
                "훈련 종료 연도": training.findtext("traEndDate", "N/A")[:4] if training.findtext("traEndDate", "N/A") != "N/A" else "N/A"
            })

        page_num += 1
        time.sleep(0.5)

    return results

# ✅ 훈련 과정 상세 정보 조회 함수 (시설 정보 + 장비 정보 포함)
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
                "시설 수": "N/A",
                "인원 수(명)": "N/A",
                "시설명": "N/A",
                "훈련기관 ID": "N/A",
                "등록훈련기관명": "N/A",
                "장비명": "N/A",
                "보유 수량": "N/A",
                "장비 등록훈련기관": "N/A"
            })
            results.append(course)
            continue

        params = {
            "authKey": auth_key,
            "returnType": "XML",  # ✅ XML 응답으로 변경
            "outType": "2",
            "srchTrprId": trpr_id,
            "srchTrprDegr": trpr_degr,
            "srchTorgId": inst_cd
        }

        response = requests.get(detail_url, params=params)

        if response.status_code == 200:
            try:
                root = ET.fromstring(response.text)  # ✅ XML 파싱

                # ✅ NCS 정보
                inst_base_info = root.find(".//inst_base_info")
                if inst_base_info is not None:
                    course.update({
                        "NCS 코드": inst_base_info.findtext("ncsCd", "N/A"),
                        "NCS 명": inst_base_info.findtext("ncsNm", "N/A"),
                        "NCS 여부": inst_base_info.findtext("ncsYn", "N/A"),
                        "정부지원금": inst_base_info.findtext("perTrco", "N/A"),
                        "총 훈련일수": inst_base_info.findtext("trDcnt", "N/A")
                    })

                # ✅ 상세 훈련 시간
                inst_detail_info = root.find(".//inst_detail_info")
                if inst_detail_info is not None:
                    course.update({
                        "총 훈련시간": inst_detail_info.findtext("totTraingTime", "N/A")
                    })

                # ✅ 시설 상세 정보 (inst_facility_info)
                inst_facility_info = root.find(".//inst_facility_info_list")
                if inst_facility_info is not None:
                    course.update({
                        "시설 면적(㎡)": inst_facility_info.findtext("fcltyArCn", "N/A"),
                        "시설 수": inst_facility_info.findtext("holdQy", "N/A"),
                        "인원 수(명)": inst_facility_info.findtext("ocuAcptnNmprCn", "N/A"),
                        "시설명": inst_facility_info.findtext("trafcltyNm", "N/A"),
                        "훈련기관 ID": inst_facility_info.findtext("cstmrId", "N/A"),
                        "등록훈련기관명": inst_facility_info.findtext("cstmrNm", "N/A")
                    })

                # ✅ 장비 상세 정보 (inst_eqmn_info)
                inst_eqmn_info = root.find(".//inst_eqmn_info_list")
                if inst_eqmn_info is not None:
                    course.update({
                        "장비명": inst_eqmn_info.findtext("eqpmnNm", "N/A"),
                        "보유 수량": inst_eqmn_info.findtext("holdQy", "N/A"),
                        "장비 등록훈련기관": inst_eqmn_info.findtext("cstmrNm", "N/A")
                    })

            except ET.ParseError:
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
