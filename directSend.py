import requests
import json
import env
from pprint import pprint
from datetime import datetime, timedelta

def fun_direct_send(sender, sendMail, receiveMail, title, newsTop, newsBottom, body):
    # 값이 모두 잘 들어왔는지 확인
    if not all([sender, sendMail, receiveMail, title, newsTop, newsBottom, body]):
        missing = [name for name, value in locals().items() if value is None or value == ""]
        return f"필수 정보가 누락되었습니다: {', '.join(missing)}."
    
    url = "https://directsend.co.kr/index.php/api_v2/mail_change_word"
    return_url = 55  # 예시 값

    url_parameters = {
        "subject": title,
        "body": f"{newsTop}\n{body}\n{newsBottom}",
        "sender": sendMail,
        "sender_name": sender,
        "username": "unionc",
        "receiver": receiveMail,
        "key": "w4EzdnbOY3oypxO",
        "return_url_yn": True,
        "return_url": return_url
    }

    try:
        response = requests.post(url, json=url_parameters)
        response_data = response.json()
        if response_data.get("status") == "0":
            print("메일이 정상적으로 보내졌습니다.")
            return response_data
        else:
            print("메일을 보내는 중 오류가 발생했습니다.")
            return response_data
    except Exception as e:
        print(f"메일 전송 중 예외가 발생했습니다: {e}")
        return "메일 전송 중 예외가 발생했습니다."

print(fun_direct_send(
    sender="김선우",
    sendMail="ksw06086@naver.com", 
    receiveMail=[{"email": "ksw04180@gmail.com"}], 
    title="쇼박스 | 2022년 11월 2일 뉴스클리핑", 
    newsTop="안녕하세요 뉴스샘플입니다.", 
    newsBottom="샘플을 원하시면 언제든 연락주세요!", 
    body="<body><div style='background-color: pink;'>안녕! 별다른 건 아니고 잠깐 니 생각이 난거야~</div></body>"
))
