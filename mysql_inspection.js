const mysql = require('mysql');

const connection = mysql.createConnection({
    host: 'movieboarddb-instance-1-ap-northeast-2a.cfkil9wmpx0x.ap-northeast-2.rds.amazonaws.com',
    user: 'admin',
    password: 'uni1004!',
    database: 'movieboard'
});

connection.connect();

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
        fetchNewRecords(lastCheckedId, (newRecords) => {
            if (newRecords.length > 0) {
                console.log("New records found:", newRecords);
                lastCheckedId = Math.max(...newRecords.map(record => record.idx));
                console.log(lastCheckedId);
            }
        });
    }, 3000); // 10초마다 데이터베이스 확인
}

main();