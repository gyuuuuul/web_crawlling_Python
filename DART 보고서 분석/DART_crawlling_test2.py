import os
import requests
import json
import pandas as pd
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

def crawldart(crp_cd, bsn_tp, sub_menu):
    base_url = "http://example.com/api?"
    auth_key = "your_auth_key"
    start_dt = "20220101"
    page_set = 10

    url = f'{base_url}{auth_key}&start_dt={start_dt}&crp_cd={crp_cd}&bsn_tp={bsn_tp}&page_set={page_set}'
    print(url)
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"API request failed with status code {response.status_code}")
        return

    try:
        data = json.loads(response.content)
    except json.JSONDecodeError as e:
        print("JSON Decode Error:", e)
        return

    total_page = data.get('total_page', 0)
    page_list = data.get('list', [])

    for i in range(2, total_page + 1):
        response = requests.get(f"{url}&page_no={i}")
        if response.status_code == 200:
            data = json.loads(response.content)
            page_list += data.get('list', [])

    df_all = pd.DataFrame()
    columnlist = ['성명(명칭)', '생년월일 또는 사업자등록번호 등', '변동일', '취득/처분방법',
                  '주식등의 종류', '변동전', '증감', '변동후', '취득/처분 단가', '비고']

    for i, each_doc in enumerate(page_list, 1):
        print(f"Processing {i}/{len(page_list)}")
        html_url = f'http://dart.fss.or.kr/dsaf001/main.do?rcpNo={each_doc["rcp_no"]}'
        req = requests.get(html_url)

        try:
            dcm_body = req.text.split(f'text: "{sub_menu}"')[1].split("viewDoc(")[1].split(")")[0]
            dcm_body_list = dcm_body.replace("'", "").replace(" ", "").split(",")
            each_doc.update({
                'dcmNo': dcm_body_list[1],
                'eleId': dcm_body_list[2],
                'offset': dcm_body_list[3],
                'length': dcm_body_list[4],
                'dtd': dcm_body_list[5],
            })
        except IndexError:
            logger.debug(f"Parsing failed: {html_url}")
            continue

        viewer_url = 'http://dart.fss.or.kr/report/viewer.do?rcpNo={rcpNo}&dcmNo={dcmNo}&eleId={eleId}&offset={offset}&length={length}&dtd={dtd}'.format(
            **each_doc)
        req = requests.get(viewer_url)
        soup = BeautifulSoup(req.text, "html.parser")

        try:
            table = soup.find("table")
            df = pd.read_html(str(table))[0]
            df.columns = columnlist
            df.insert(0, 'RMK', each_doc.get('rmk', ''))
            df.insert(0, '보고서명', each_doc.get('rpt_nm', ''))
            df.insert(0, '공시대상회사', each_doc.get('crp_nm', ''))
            df.insert(0, '제출인', each_doc.get('flr_nm', ''))
            df.insert(0, '접수일자', each_doc.get('rcp_dt', ''))
            df_all = pd.concat([df_all, df], ignore_index=True)
        except Exception as e:
            logger.debug(f"Failed to parse table: {viewer_url}, Error: {e}")
            continue

    os.makedirs('./output', exist_ok=True)
    df_all.to_csv(f'./output/{crp_cd}_{bsn_tp}_{sub_menu}.csv', index=False)

# Example usage
crawldart("005930", "D001", "세부변동내역")
