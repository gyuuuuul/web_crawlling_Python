import openai

# API 키 설정
openai.api_key = "-보안사항-push 안됨됨"

client = openai.OpenAI(api_key=openai.api_key)

try:
    # ChatCompletion 요청
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Who won the world series in 2020?"}
        ]
    )

    # 응답 출력
    print("응답 내용:")
    print(response.choices[0].message.content)  # ChatCompletion 객체의 속성을 통해 접근
except openai.error.OpenAIError as e:
    print(f"OpenAI API 호출 중 오류가 발생했습니다: {e}")
except Exception as e:
    print(f"일반 오류가 발생했습니다: {e}")
