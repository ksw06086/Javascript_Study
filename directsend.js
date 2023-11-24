async function funDirectSend() {
    const url = "https://directsend.co.kr/index.php/api_v2/mail_change_word";

    // 필수입력
    const subject = "제목입니다.";
    const body = "<body><div style='background-color: pink;'>안녕! 별다른 건 아니고 잠깐 니 생각이 난거야~</div></body>";
    const sender = "ksw06086@naver.com";
    const sender_name = "김선우";

    const receiver = JSON.stringify({ "email": "ksw04180@gmail.com" });
    const return_url = 55;  // 예시 값

    const urlParameters = {
        subject: subject,
        body: body,
        sender: sender,
        sender_name: sender_name,
        username: "unionc",
        receiver: [receiver],
        key: "w4EzdnbOY3oypxO",
        return_url_yn: true,
        return_url: return_url
    };

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Cache-Control': 'no-cache',
                'Content-Type': 'application/json;charset=utf-8',
                'Accept': 'application/json'
            },
            body: JSON.stringify(urlParameters)
        });
        const responseData = await response.json();
        if (responseData.status === "0") {
            console.log("메일이 정상적으로 보내졌습니다.");
            return "메일이 정상적으로 보내졌습니다.";
        } else {
            return "메일을 보내는 중 오류가 발생했습니다.";
        }
    } catch (error) {
        console.error(error);
        return "메일 전송 중 예외가 발생했습니다.";
    }
}

funDirectSend()