import dart_fss as dart_fss
import pandas as pd
import requests
import os
from lxml import html
import re
from utils import *
from subprocess import call
from fake_useragent import UserAgent
import webbrowser


# DART KEY 설정
api_key = '2793c614ecaf8467a0f2e18e3268332f701237e0'
dart_fss.set_api_key(api_key=api_key)

# 사용자 입력 받기
corp_name = input("기업명을 입력하세요: ")
pblntf_type = input("공시유형을 선택하세요. (A : 정기공시 B : 주요사항보고 C : 발행공시 D : 지분공시 E : 기타공시 F : 외부감사관련 G : 펀드공시 H : 자산유동화 I : 거래소공시 J : 공정위공시 중 1개): ")
start_date = input("공시보고서 시작일을 입력하세요 (YYYYMMDD 형식): ")
end_date = input("공시보고서 마감일을 입력하세요 (YYYYMMDD 형식): ")
file_name = input("저장할 파일 이름을 입력하세요 (.xlsx 형식): ")

# Desktop 경로 설정
desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
save_dir = os.path.join(desktop, corp_name)
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# 상장 기업명 크롤링
corp_list = dart_fss.api.filings.get_corp_code()
corp_df = pd.DataFrame.from_dict(corp_list)
corp_df = corp_df.dropna(subset=['stock_code']).sort_values('modify_date', ascending=False).reset_index(drop=True)
corp_df['done_YN'] = "N"


# 입력한 기업명에 해당하는 corp_code 가져오기
try:
    corp_code = corp_df.loc[corp_df['corp_name'] == corp_name, 'corp_code'].values[0]
except IndexError:
    print("입력한 기업명을 찾을 수 없습니다. 다시 확인하세요.")
    exit()

# API 요청 URL
url_json = "https://opendart.fss.or.kr/api/list.json"

# API 요청 파라미터
params = {
    'crtfc_key': api_key,
    'corp_code': corp_code,
    'pblntf_ty': pblntf_type, # 공시유형(A를 주로 사용)
    'bgn_de': start_date,  # 공시보고서 시작일
    'end_de': end_date # 공시보고서 종료일
}

# API 요청
response = requests.get(url_json, params=params)
res = response.json()

if res['status'] == '013':
    print(f"{corp_name}의 사업보고서 개수가 없습니다.")
    exit()

# 데이터프레임 생성 및 저장
try:
    df_imsi = pd.DataFrame(res['list'])
except KeyError:
    print("API 응답에 리스트가 없습니다. 다시 확인하세요.")
    exit()

# 파일 저장 경로
file_listed = os.path.join(desktop, file_name)

# 엑셀로 저장
df_imsi.to_excel(file_listed, index=False)
print(f"파일이 저장되었습니다: {file_listed}")


# 파일 다운로드 함수
def download_file(url, file_path, file_type):
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_path, "wb") as file:
            file.write(response.content)
        print(f"{file_type} 저장: {file_path}")
    else:
        print(f"{file_type} 다운로드 실패. 상태 코드: {response.status_code}")

# HTML에서 보고서 이름과 dcm_no 추출
def extract_report_details(rcp_no):
    url = f"http://dart.fss.or.kr/dsaf001/main.do?rcpNo={rcp_no}"
    response = requests.get(url)
    if response.status_code == 200:
        tree = html.fromstring(response.content)
        try:
            # 보고서 이름 추출 (<title> 태그)
            title_text = tree.xpath('//title/text()')[0]
            report_name = title_text.split("/")[1]  # "분기보고서" 등 추출

            # dcm_no 추출
            onclick_data = tree.xpath('//button[@class="btnDown"]/@onclick')[0]
            dcm_no = re.search(r"openPdfDownload\('\d+', '(\d+)'\)", onclick_data).group(1)
            
            return report_name, dcm_no
        except (IndexError, AttributeError):
            print(f"보고서 이름 또는 dcm_no를 추출할 수 없습니다: {url}")
            return None, None
    else:
        print(f"HTML 요청 실패. 상태 코드: {response.status_code}")
        return None, None

# 파일 다운로드 처리
for index, row in df_imsi.iterrows():
    rcept_no = row['rcept_no']  # rcept_no 추출
    report_name, dcm_no = extract_report_details(rcept_no)  # HTML에서 dcm_no 추출
    if not dcm_no:
        print(f"dcm_no를 찾을 수 없습니다. 보고서 번호: {rcept_no}")
        continue
    
    report_date = row['rcept_dt']  # 보고서 날짜

    # PDF 다운로드 URL
    pdf_url = f"http://dart.fss.or.kr/pdf/download/pdf.do?rcp_no={rcept_no}&dcm_no={dcm_no}"
    print(f"PDF 다운로드 URL을 열고 있습니다: {pdf_url}")
    webbrowser.open(pdf_url)

    # Excel 다운로드 URL
    excel_url = f"http://dart.fss.or.kr/pdf/download/excel.do?rcp_no={rcept_no}&dcm_no={dcm_no}&lang=ko"
    print(f"Excel 다운로드 URL을 열고 있습니다: {excel_url}")
    webbrowser.open(excel_url)

    # IFRS 다운로드 URL
    ifrs_url = f"http://dart.fss.or.kr/pdf/download/ifrs.do?rcp_no={rcept_no}&dcm_no={dcm_no}&lang=ko"
    print(f"IFRS 다운로드 URL을 열고 있습니다: {ifrs_url}")
    webbrowser.open(ifrs_url)
    
