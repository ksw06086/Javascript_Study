// * 문자형으로 변환
let value = true;
alert(typeof value); // boolean

value = String(value); // 변수 value엔 문자열 "true"가 저장됩니다.
alert(typeof value); // string

// * 숫자형으로 변환
// 정상
alert( "6" / "2" ); // 3, 문자열이 숫자형으로 자동변환된 후 연산이 수행됩니다.
// 정상
let str = "123";
alert(typeof str); // string
let num = Number(str); // 문자열 "123"이 숫자 123으로 변환됩니다.
alert(typeof num); // number
//! 오류
let age = Number("임의의 문자열 123");
alert(age); // NaN, 형 변환이 실패합니다.

// * 불린형으로 변환
alert( Boolean(1) ); // 숫자 1(true)
alert( Boolean(0) ); // 숫자 0(false)

alert( Boolean("hello") ); // 문자열(true)
alert( Boolean("") ); // 빈 문자열(false)


