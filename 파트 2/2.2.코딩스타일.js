//? 스타일 가이드
// # Google의 자바스크립트 스타일 가이드 
'https://google.github.io/styleguide/jsguide.html'
// # StandardJS
'https://standardjs.com/'

//? Linter
// # Linter라는 도구를 사용하면 내가 작성한 코드가 스타일 가이드를 준수하고 있는지를 자동으로 확인할 수 있고, 
// # 스타일 개선과 관련된 제안도 받을 수 있습니다.

// * ESLint – 가장 최근에 나온 linter
'https://eslint.org/'

// * ESLint를 사용한다고 가정했을 때 아래 절차를 따르면 에디터와 linter를 통합해 사용할 수 있습니다.
// # 1. Node.js를 설치합니다.
// # 2. npm(자바스크립트 패키지 매니저)을 사용해 다음 명령어로 ESLint를 설치합니다. npm install -g eslint
// # 3. 현재 작성 중인 자바스크립트 프로젝트의 루트 폴더(프로젝트 관련 파일이 담긴 폴더)에 .eslintrc라는 설정 파일을 생성합니다.
// # 4. 에디터에 ESLint 플러그인을 설치하거나 활성화합니다. 주요 에디터들은 모두 ESLint 플러그인을 지원합니다.

// * .eslintrc 파일의 예시
// {
//     "extends": "eslint:recommended",
//     "env": {
//         "browser": true,
//         "node": true,
//         "es6": true
//     },
//     "rules": {
//         "no-console": 0,
//         "indent": ["warning", 2]
//     }
// }