const mysql = require('mysql');

const connection = mysql.createConnection({
    host: 'movieboarddb-instance-1-ap-northeast-2a.cfkil9wmpx0x.ap-northeast-2.rds.amazonaws.com',
    user: 'admin',
    password: 'uni1004!',
    database: 'movieboard'
});

connection.connect();

async function funDirectSend(subject, send_mail, sender_name, receive_mail, body, mail_group) {
    const url = "https://directsend.co.kr/index.php/api_v2/mail_change_word";

    // 필수입력
    // const subject = "제목입니다.";
    // const body = "<body><div style='background-color: pink;'>안녕! 별다른 건 아니고 잠깐 니 생각이 난거야~</div></body>";
    // const sender = "ksw06086@naver.com";
    // const sender_name = "김선우";

    const receiver = JSON.stringify({ "email": receive_mail });
    const return_url = 55;  // 예시 값

    console.log(subject, send_mail, sender_name, body, receive_mail, mail_group);
    if(mail_group != null) console.log("메일그룹이 있습니다.");
    else console.log("메일그룹이 없습니다.");

    const urlParameters = {
        subject: subject,
        body: body,
        sender: send_mail,
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
            return "메일이 정상적으로 보내졌습니다.";
        } else {
            return "메일을 보내는 중 오류가 발생했습니다.";
        }
    } catch (error) {
        console.error(error);
        return "메일 전송 중 예외가 발생했습니다.";
    }
}

function fetchNewRecords(lastCheckedId, callback) {
    const query = "SELECT * FROM mail_log WHERE idx > ?";
    connection.query(query, [lastCheckedId], (err, results) => {
        if (err) throw err;
        callback(results);
    });
}

function main() {
    let lastCheckedId = 0;
    fetchNewRecords(lastCheckedId, (newRecords) => {
        lastCheckedId = Math.max(...newRecords.map(record => record.idx));
    });

    setInterval(() => {
        fetchNewRecords(lastCheckedId, async (newRecords) => {
            if (newRecords.length > 0) {
                console.log("New records found:", newRecords);
                lastCheckedId = Math.max(...newRecords.map(record => record.idx));
                console.log(lastCheckedId);
                const result = [...newRecords.map( async record => await funDirectSend(record.title, record.send_mail, record.sender, record.receive_mail, record.body, record.mail_group))];
                console.log(result);
            }
        });
    }, 3000); // 10초마다 데이터베이스 확인
}

main();

// 매 시간마다 mysql을 검사하고 최근 로그가 있으면 메일을 전송함
// 