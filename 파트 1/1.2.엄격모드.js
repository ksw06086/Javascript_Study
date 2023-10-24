//? use strict(엄격모드) 꼭 사용해야 하나?
// 모던 자바스크립트는 '클래스’와 '모듈’이라 불리는 진일보한 구조를 제공합니다
// (클래스와 모듈에 대해선 당연히 뒤에서 학습할 예정입니다). 
// 이 둘을 사용하면 use strict가 자동으로 적용되죠. 
// 따라서 이 둘을 사용하고 있다면 스크립트에 "use strict"를 붙일 필요가 없습니다.

//! 오류 발생
x = 3.14; // 오류: x is not defined
//? 정상 실행
"use strict";
x = 3.14; // 오류: x is not defined

// * 엄격한 모드를 사용하면 다음과 같은 변경 사항이 적용됨
// * 1. 변수를 선언하지 않고 사용하면 오류가 발생합니다.
// ? 정상 실행
x = 3.14; // 오류: x is not defined
// * 2. 익명 함수의 매개 변수 이름을 중복하면 오류가 발생합니다.
​// ? 정상 실행
function example(a, a) { // 오류: Duplicate parameter name not allowed in this context
    // ...
}
// * 3. 읽기 전용 속성을 변경하려고 하면 오류가 발생합니다.
​// ? 정상 실행
var obj = {
    get prop() {
       return 'value';
    }
};
Object.defineProperty(obj, 'prop', {
value: 'newvalue', // 오류: Cannot redefine property: prop
});

