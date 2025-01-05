import dart_fss as dart_fss
import pandas as pd
import os

# Desktop 경로 설정
desktop = os.path.join(os.path.expanduser('~'), 'Desktop')

# DART KEY 구동
api_key = '2793c614ecaf8467a0f2e18e3268332f701237e0'
dart_fss.set_api_key(api_key=api_key)

# 전체 종목을 보는 코드
all = dart_fss.api.filings.get_corp_code()

df = pd.DataFrame(all)

# 상장사, 비 상장사 나누기. stock-code가 notnull이면 상장사.
df_listed = df[df['stock_code'].notnull()]
df_non_listed = df[df['stock_code'].isnull()]


# 파일 저장 경로 설정
file_listed = os.path.join(desktop, '상장사.xlsx')
file_non_listed = os.path.join(desktop, '비상장사.xlsx')


df_listed.to_excel(file_listed, index = False)
df_non_listed.to_excel(file_non_listed, index = False)

# 이 때, 결과는 상장사의 경우, corp_code, corp_name, stock_code, modify_date 가 나오고,
# 비상장사의 경우: stock_code가 null로 생성


