// * 세미콜론(;)
// 가능
alert('Hello')
alert('World')

// 가능
alert(3 +
    1
    + 2);

// * [...]앞에는 세미콜론이 있다고 가정하지 않음
//! 에러 발생
alert("에러가 발생합니다.")
[1, 2].forEach(alert)
//! => alert("에러가 발생합니다.")[1, 2].forEach(alert)
//? 정상
alert("제대로 동작합니다.");
[1, 2].forEach(alert)