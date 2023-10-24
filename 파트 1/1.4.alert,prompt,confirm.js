// * alert
alert("Hello");

// * prompt
// result = prompt(title, [default]);
let age = prompt('나이를 입력해주세요.', 100);
alert(`당신의 나이는 ${age}살 입니다.`); // 당신의 나이는 100살입니다.

// * confirm
// result = confirm(question);
let isBoss = confirm("당신이 주인인가요?");
alert( isBoss ); // 확인 버튼을 눌렀다면 true가 출력됩니다.