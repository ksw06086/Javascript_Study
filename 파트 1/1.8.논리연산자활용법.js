//? &&를 사용한 코드가 더 짧긴 하지만 if문을 사용한 예시가 코드에서 무엇을 구현하고자 하는지 더 명백히 드러내고, 가독성도 좋습니다.

// * 첫 번째 truthy를 찾는 OR 연산자 ‘||’

// * 1
let firstName = "";
let lastName = "";
let nickName = "바이올렛";

alert( firstName || lastName || nickName || "익명"); // 바이올렛

// * 2
true || alert("not printed");
false || alert("printed"); // 이것만 alert이 뜸

// * 첫 번째 falsy를 찾는 AND 연산자 ‘&&’
// 가장 왼쪽 피연산자부터 시작해 오른쪽으로 나아가며 피연산자를 평가

// * 첫 번째 피연산자가 truthy이면,
// * AND는 두 번째 피연산자를 반환합니다.
alert( 1 && 0 ); // 0
alert( 1 && 5 ); // 5
alert( 1 && 2 && 3 ); // 마지막 값, 3

// * 첫 번째 피연산자가 falsy이면,
// * AND는 첫 번째 피연산자를 반환하고, 두 번째 피연산자는 무시합니다.
alert( null && 5 ); // null
alert( 0 && "아무거나 와도 상관없습니다." ); // 0

// * 중간의 피연산자가 falsy이면
alert( 1 && 2 && null && 3 ); // null