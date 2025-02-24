import requests
import time
import pandas as pd
import os

# 바탕화면 경로 설정 (Windows 기준)
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

# API 키 설정
Auth_Key = "Pep4ggqqRYTyJrUldJTJeEnQNFVnAyJArPXMFpLdePliuKRvz69vSqYzzuwXFJXWEmM5osRjqtKGFDqw1f9ahw=="

# 요청 URL (관광객 데이터 조회)
REQUEST_URL = "http://apis.data.go.kr/B551011/DataLabService/metcoRegnVisitrDDList"

# 사용자 입력 받기
start_date = input("조회시작연월일(yyyyMMdd): ")
end_date = input("조회종료연월일(yyyyMMdd): ")

# 한 페이지당 출력 개수 (표 예시 기준 10)
page_size = 100
results = []

page_num = 1
while True:
    params = {
        "serviceKey": Auth_Key,            
        "_type": "Json",            
        "MobileOS": "ETC",
        "MobileApp": "AppTest",
        "pageNo": str(page_num),        
        "numOfRows": str(page_size),      
        "startYmd": start_date,  
        "endYmd": end_date  
    }

    response = requests.get(REQUEST_URL, params=params)
    
    if response.status_code != 200:
        print(f"❌ 오류 발생: {response.status_code}")
        print("응답 내용:", response.text)
        break  

    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError:
        print("⚠️ JSON 디코딩 오류 발생! 응답이 JSON 형식이 아닙니다.")
        print("응답 내용:", response.text)
        break

    # 응답 구조가 'response' 키를 포함하는지 확인
    if "response" not in data:
        print("⚠️ 응답 데이터에 'response' 키가 없습니다.")
        break

    header = data["response"].get("header", {})
    body = data["response"].get("body", {})

    # 첫 페이지에서 메타데이터 출력
    if page_num == 1:
        print("📌 응답 메타데이터:")
        print(f"resultCode\t결과코드\t1\t{header.get('resultCode', 'N/A')}\t응답 결과코드")
        print(f"resultMsg\t결과메시지\t1\t{header.get('resultMsg', 'N/A')}\t응답 결과메시지")
        print(f"numOfRows\t한 페이지 결과 수\t1\t{body.get('numOfRows', 'N/A')}\t한 페이지 결과 수")
        print(f"pageNo\t페이지 번호\t1\t{body.get('pageNo', 'N/A')}\t현재 페이지 번호")
        print(f"totalCount\t전체 결과 수\t1\t{body.get('totalCount', 'N/A')}\t전체 결과 수")
        print()

    # 관광객 데이터 추출 (items.item)
    items = body.get("items", {}).get("item")
    
    if not items:
        print("⚠️ 더 이상 검색된 데이터가 없습니다.")
        break

    # 한 건만 dict로 올 경우 리스트로 변환
    if isinstance(items, dict):
        items = [items]

    for item in items:
        results.append({
            "areaCode": item.get("areaCode", "N/A"),
            "areaNm": item.get("areaNm", "N/A"),
            "daywkDivCd": item.get("daywkDivCd", "N/A"),
            "daywkDivNm": item.get("daywkDivNm", "N/A"),
            "touDivCd": item.get("touDivCd", "N/A"),
            "touDivNm": item.get("touDivNm", "N/A"),
            "touNum": item.get("touNum", "N/A"),
            "baseYmd": item.get("baseYmd", "N/A")
        })

    totalCount = int(body.get("totalCount", 0))
    if len(results) >= totalCount:
        break
    else:
        page_num += 1
        print(f"✅ {page_num - 1} 페이지 완료, 다음 페이지 요청 중...")
        #time.sleep(0.1)

# 출력: 표 형식으로 (첫번째 데이터 건 예시)
if results:
    
    # 바탕화면에 엑셀 저장 (전체 데이터)
    excel_filename = os.path.join(desktop_path, "한국관광공사_관광객_데이터.xlsx")
    df = pd.DataFrame(results)
    df.to_excel(excel_filename, index=False, engine="openpyxl")
    print(f"\n📁 엑셀 파일 저장 완료: {excel_filename}")
else:
    print("❌ 검색된 데이터가 없습니다.")
