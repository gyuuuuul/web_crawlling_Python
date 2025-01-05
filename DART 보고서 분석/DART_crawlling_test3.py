import dart_fss as dart_fss
import pandas as pd
import requests
import os
from lxml import html
import re
from utils import *
from subprocess import call
from fake_useragent import UserAgent


# DART KEY 설정
api_key = '2793c614ecaf8467a0f2e18e3268332f701237e0'
dart_fss.set_api_key(api_key=api_key)

# 사용자 입력 받기
corp_name = input("기업명을 입력하세요: ")
pblntf_type = input("공시유형을 선택하세요. (A : 정기공시 B : 주요사항보고 C : 발행공시 D : 지분공시 E : 기타공시 F : 외부감사관련 G : 펀드공시 H : 자산유동화 I : 거래소공시 J : 공정위공시 중 1개): ")
start_date = input("공시보고서 시작일을 입력하세요 (YYYYMMDD 형식): ")
end_date = input("공시보고서 마감일을 입력하세요 (YYYYMMDD 형식): ")
file_name = input("저장할 파일 이름을 입력하세요 (.xlsx 형식): ")
bsn_tp = "A001"

# Desktop 경로 설정
desktop = os.path.join(os.path.expanduser('~'), 'Desktop')

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

# 사업보고서 xml zip파일 다운로드"
url_zip = "https://opendart.fss.or.kr/api/document.xml"


for index, row in df_imsi.iterrows():
    rcept_no = row['rcept_no']  # rcept_no 추출
    
    # API 요청 파라미터
    params2 = {
        'crtfc_key': api_key,
        'rcept_no': rcept_no
    }
    
    # API 요청
    response_zip = requests.get(url_zip, params=params2)
    
    if response_zip.status_code == 200:
        # ZIP 파일 저장 경로
        zip_file_name = f"{rcept_no}.zip"
        zip_file_path = os.path.join(desktop, zip_file_name)
        
        # ZIP 파일 저장
        with open(zip_file_path, 'wb') as f:
            f.write(response_zip.content)
        print(f"ZIP 파일이 저장되었습니다: {zip_file_path}")
        
        # ZIP 파일 추출
        extract_dir = os.path.join(desktop, rcept_no)
        if not os.path.exists(extract_dir):
            os.makedirs(extract_dir)
        
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
        print(f"ZIP 파일이 추출되었습니다: {extract_dir}")
        
        # XML 파일 읽기 및 처리
        xml_files = [file for file in os.listdir(extract_dir) if file.endswith('.xml')]
        if xml_files:
            xml_file_path = os.path.join(extract_dir, xml_files[0])
            try:
                with open(xml_file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                print(f"XML 파일 내용:\n{content[:500]}")  # 파일 첫 500자 출력
                
                # 특수 문자 처리
                cleaned_content = content.replace('&', '&amp;')
                
                # XML 파싱
                parser = etree.XMLParser(recover=True, encoding='utf-8')
                root = etree.fromstring(cleaned_content.encode('utf-8'), parser=parser)
                print(f"XML 파싱 성공! 루트 태그: {root.tag}")
            except Exception as e:
                print(f"XML 처리 중 오류 발생: {e}")
        else:
            print("ZIP 파일에 XML 파일이 없습니다.")
    else:
        print(f"{rcept_no} 보고서 다운로드 실패: {response_zip.status_code}")
        print("응답 내용:", response_zip.text)