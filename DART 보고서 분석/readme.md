파이썬으로 DART 산업보고서 분석 및 데이터 크롤링하기.

1차적으로는 분석이 목표,

추후 AI를 활용한 분석까지 만드는 것이 목표이다.


해야할일

1. DART OPEN API 신청

키 발급
https://opendart.fss.or.kr/uat/uia/egovLoginUsr.do

에서 회원가입 후 오픈 API 이용현황에서 API KEY 를 확인한다.

2. dart-fss 설치
cmd에 "pip install dart-fss" 입력 후 설치

3. 키 넣고 구동해보기

import dart_fss as dart_fss
import pandas as pd

api_key = '여기에 API 키를 입력'
dart_fss.set_api_key(api_key=api_key)

corp_list = dart_fss.get_corp_list()

corp_list.corps

4. Dart 공식 Document: https://dart-fss.readthedocs.io/en/latest/


참고
https://github.com/seoweon/dart_reports


공시검색 가이드
https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS001&apiId=2019001
