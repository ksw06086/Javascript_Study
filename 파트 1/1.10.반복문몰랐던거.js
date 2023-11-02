//? ‘?’ 오른쪽엔 break나 continue가 올 수 없습니다.
(i > 5) ? alert(i) : continue; //# 여기에 continue를 사용하면 안 됩니다.


//? 레이블
//# 수정 전
for (let i = 0; i < 3; i++) {
    for (let j = 0; j < 3; j++) {
      let input = prompt(`(${i},${j})의 값`, '');
  
      //# 여기서 멈춰서 아래쪽의 `완료!`가 출력되게 하려면 어떻게 해야 할까요?
    }
  }
  alert('완료!');

//# 수정 후
outer: for (let i = 0; i < 3; i++) {
    for (let j = 0; j < 3; j++) {
      let input = prompt(`(${i},${j})의 값`, '');
  
      //# 사용자가 아무것도 입력하지 않거나 Cancel 버튼을 누르면 두 반복문 모두를 빠져나옵니다.
      if (!input) break outer; // (*)
  
      //# 입력받은 값을 가지고 무언가를 함
    }
  }
  alert('완료!');

//? 레이블은 마음대로 '점프’할 수 있게 해주지 않습니다.
break label; //# 아래 for 문으로 점프할 수 없습니다.
label: for (...)