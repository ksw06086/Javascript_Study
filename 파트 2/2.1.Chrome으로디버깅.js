//? ‘Sources’ 패널
// # F12(MacOS: Cmd+Opt+I)를 눌러 개발자 도구를 엽니다.
// # Sources 탭을 클릭해 Sources 패널(panel)을 엽니다.

//? debugger 명령어
function hello(name) {
    let phrase = `Hello, ${name}!`;

    debugger;  // <-- 여기서 실행이 멈춥니다.

    say(phrase);
}

//? Source 탭에서 보이는 것들
// # 1. Watch – 표현식을 평가하고 결과를 보여줍니다.
// # 2. Call Stack – 코드를 해당 중단점으로 안내한 실행 경로를 역순으로 표시합니다.
// # 3. Scope – 현재 정의된 모든 변수를 출력합니다.
    // # Local은 함수의 지역변수를 보여줍니다. 지역 변수 정보는 소스 코드 영역에서도 확인(강조 표시)할 수 있습니다.
    // # Global은 함수 바깥에 정의된 전역 변수를 보여줍니다.
    // # Local 하위 항목으로 this에 대한 정보도 출력되는데, 이에 대해선 추후에 학습하도록 하겠습니다.

