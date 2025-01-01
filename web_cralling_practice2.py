# requests 패키지 가져오기
import requests      

# BeautifulSoup 패키지 불러오기
# 주로 bs로 이름을 간단히 만들어서 사용함
from bs4 import BeautifulSoup as bs

# 가져올 url 문자열로 입력
url = 'https://www.naver.com'  

# requests의 get함수를 이용해 해당 url로 부터 html이 담긴 자료를 받아옴
response = requests.get(url)    

# 우리가 얻고자 하는 html 문서가 여기에 담기게 됨
html_text = response.text

# html을 잘 정리된 형태로 변환
html = bs(html_text, 'html.parser')

print(html.title.text)