//? nullish 병합 연산자 '??'
a ?? b //# a가 null도 아니고 undefined도 아니면 a 그 외의 경우는 b

let firstName = null;
let lastName = null;
let nickName = "바이올렛";

//# null이나 undefined가 아닌 첫 번째 피연산자
alert(firstName ?? lastName ?? nickName ?? "익명의 사용자"); //# 바이올렛

//? '??'와 '||'의 차이
//# null과 undefined, 숫자 0을 구분 지어 다뤄야 할 때 이 차이점은 매우 중요한 역할을 합니다.
let height = 0;

alert(height || 100); // 100
alert(height ?? 100); // 0