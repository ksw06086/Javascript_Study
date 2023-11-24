// <head></head> 안에 들어갈 부분
// <!-- 결과 출력에 사용되는 mocha css를 불러옵니다. -->
// <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/mocha/3.2.0/mocha.css">
// <!-- Mocha 프레임워크 코드를 불러옵니다. -->
// <script src="https://cdnjs.cloudflare.com/ajax/libs/mocha/3.2.0/mocha.js"></script>
// <script>
// mocha.setup('bdd'); // 기본 셋업
// </script>
// <!-- chai를 불러옵니다 -->
// <script src="https://cdnjs.cloudflare.com/ajax/libs/chai/3.5.0/chai.js"></script>
// <script>
// // chai의 다양한 기능 중, assert를 전역에 선언합니다.
// let assert = chai.assert;
// </script>

function pow(x, n) {
    /* 코드를 여기에 작성합니다. 지금은 빈칸으로 남겨두었습니다. */
}

describe("pow", function() {
    it("주어진 숫자의 n 제곱", function() {
      assert.equal(pow(2, 3), 8);
    });
});

mocha.run();