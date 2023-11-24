//? 테스트 자동화와 Mocha
//? 테스트는 왜 해야 하는가?
'구체적인 예를 들어봅시다. 현재 함수 f를 구현하고 있다고 가정해보겠습니다.'
'코드를 작성하고 f(1)이 제대로 동작하는지 확인합니다. 제대로 동작하네요. '
'그런데 f(2)를 테스트해 보니 제대로 동작하지 않습니다. '
'코드를 수정한 후 다시 f(2)를 확인해 봅니다. 제대로 동작하네요. '
'여기서 끝일까요? 아닙니다. f(1)이 제대로 동작하는지 확인하지 않았으니까요. '
'이렇게 테스트를 수동으로 하면 에러가 발생할 여지를 남깁니다.'

//? Behavior Driven Development
// BDD는 테스트(test), 문서(documentation), 예시(example)를 한데 모아놓은 개념

//? 테스트 코드 예시
describe("pow", function() {
    it("주어진 숫자의 n 제곱", function() {
        assert.equal(pow(2, 3), 8);
    });
});

//# 1. 구현하고자 하는 기능에 대한 설명
describe("title", function() { '...' })
//# 2. it의 첫 번째 인수엔 특정 유스 케이스에 대한 설명
it("유스 케이스 설명", function() { '...' })
//# 3. 실행코드
assert.equal(value1, value2)

//? 개발 순서
// # 1. 명세서 초안을 작성합니다. 초안엔 기본적인 테스트도 들어갑니다.
// # 2. 명세서 초안을 보고 코드를 작성합니다.
// # 3. 코드가 작동하는지 확인하기 위해 Mocha라 불리는 테스트 프레임워크를 사용해 명세서를 실행합니다.(Mocha에 대해선 아래에서 다룰 예정입니다.) 
// #    이때, 코드가 잘못 작성되었다면 에러가 출력됩니다. 개발자는 테스트를 모두 통과해 에러가 더는 출력되지 않을 때까지 코드를 수정합니다.
// # 4. 모든 테스트를 통과하는 코드 초안이 완성되었습니다.
// # 5. 명세서에 지금까진 고려하지 않았던 유스케이스 몇 가지를 추가합니다. 테스트가 실패하기 시작할 겁니다.
// # 6. 세 번째 단계로 돌아가 테스트를 모두 통과할 때까지 코드를 수정합니다.
// # 7. 기능이 완성될 때까지 3~6단계를 반복합니다.

//? 테스트 라이브러리
// * Mocha – 핵심 테스트 프레임워크로, describe, it과 같은 테스팅 함수와 테스트 실행 관련 주요 함수를 제공합니다.
// * Chai – 다양한 assertion을 제공해 주는 라이브러리입니다. 우리 예시에선 assert.equal 정도만 사용해 볼 예정입니다.
// * Sinon – 함수의 정보를 캐내는 데 사용되는 라이브러리로, 내장 함수 등을 모방합니다. 본 챕터에선 사용하지 않고, 다른 챕터에서 실제로 사용해 볼 예정입니다.

//? 중첩 describe -> for문을 사용하거나 그룹화 해야할 때
describe("pow", function() {

    describe("x를 세 번 곱합니다.", function() {

        function makeTest(x) {
        let expected = x * x * x;
        it(`${x}을/를 세 번 곱하면 ${expected}입니다.`, function() {
            assert.equal(pow(x, 3), expected);
        });
        }

        for (let x = 1; x <= 5; x++) {
        makeTest(x);
        }

    });

    // describe와 it을 사용해 이 아래에 더 많은 테스트를 추가할 수 있습니다.
});
// 결과
// raises x to power 3
//     1 in the power 3 is 1‣
//     2 in the power 3 is 8‣
//     3 in the power 3 is 27‣
//     4 in the power 3 is 64‣
//     5 in the power 3 is 125

//? before/after와 beforeEach/afterEach
// * before는 (전체) 테스트가 실행되기 전에 실행 / after는 (전체) 테스트가 실행된 후에 실행
// * beforeEach는 매 it이 실행되기 전에 실행 / afterEach는 매 it이 실행된 후에 실행
describe("test", function() {

    before(() => alert("테스트를 시작합니다 - 테스트가 시작되기 전"));
    after(() => alert("테스트를 종료합니다 - 테스트가 종료된 후"));
  
    beforeEach(() => alert("단일 테스트를 시작합니다 - 각 테스트 시작 전"));
    afterEach(() => alert("단일 테스트를 종료합니다 - 각 테스트 종료 후"));
  
    it('test 1', () => alert(1));
    it('test 2', () => alert(2));
  
});

//? 다양한 assertion
//* assert.equal(value1, value2) – value1과 value2의 동등성을 확인합니다(value1 == value2).
//* assert.strictEqual(value1, value2) – value1과 value2의 일치성을 확인합니다(value1 === value2).
//* assert.notEqual, assert.notStrictEqual – 비 동등성, 비 일치성을 확인합니다.
//* assert.isTrue(value) – value가 true인지 확인합니다(value === true).
//* assert.isFalse(value) – value가 false인지 확인합니다(value === false).
// # 이외 다양한 assertion : https://www.chaijs.com/api/assert/

//? 테스트 코드에 많은 it 중에서 하나만 실행하게 하고 싶다면? -> it.only
// Mocha는 아래 블록만 실행합니다.
it.only("5를 2 제곱하면 25", function() {
assert.equal(pow(5, 2), 25);
});