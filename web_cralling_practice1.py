# requests 패키지 가져오기
import requests               

# 가져올 url 문자열로 입력
url = 'https://www.naver.com'  

# requests의 get함수를 이용해 해당 url로 부터 html이 담긴 자료를 받아옴
response = requests.get(url)    

# 우리가 얻고자 하는 html 문서가 여기에 담기게 됨
html_text = response.text

print(html_text)

with open('naver.html', 'w', encoding='utf-8') as file:
    file.write(html_text)