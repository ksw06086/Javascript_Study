// * Infinity
alert( 1 / 0 ); // 무한대
alert( Infinity ); // 무한대

// * NaN
alert( "숫자가 아님" / 2 ); // NaN, 문자열을 숫자로 나누면 오류가 발생합니다.
alert( "숫자가 아님" / 2 + 5 ); // NaN

// * BigInt
// 끝에 'n'이 붙으면 BigInt형 자료입니다.
const bigInt = 1234567890123456789012345678901234567890n;

// * 문자형
let str = "Hello";
let str2 = 'Single quotes are ok too';
let phrase = `can embed another ${str}`;

// * ‘undefined’ 값
// 변수는 선언했지만, 값을 할당하지 않았다면 해당 변수에 undefined가 자동으로 할당됩니다.
let age; alert(age); // 'undefined'가 출력됩니다.

// * 객체(object)형 : 데이터 컬렉션이나 복잡한 개체(entity)를 표현
// * 심볼(symbol)형 : 객체의 고유한 식별자(unique identifier)를 만들 때 사용