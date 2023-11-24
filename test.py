text_1 = """
1) 합자타겟만남 (따기목표: 00명)
상/통/김유진-박석훈-미정/19:00/홍대/친교/
상/개/엄채영-한윤성-미정/15:00/홍대/인터뷰/(부재로 다시전화예정)
상/통/김상희-정승환-미정///전도의장/
번/개/이수연-정선아-미정/20:00/합정/전도의장:o:
이/개/손승희-서승현-미정/19:00/홍대/인터뷰/:o:
이/개/유안나-정운수-미정/20:00/홍대/전도의장/(부재로 확티 필요)
이/개/유안나-서우진-미정/20:00/홍대/전도의장/(부재로 확티 필요)
이/개/김반디-서나영-미정/19:30/홍대/전도의장/:o:
이/개/이유진B-안상준-미정/20:00/홍대/전도의장/(부재로 다시 전화예정)
이/통/이유진B-김봉주-미정/16:00/홍대/친교/:o:
이/지/정준호-이태로-미정/19:00/광명/친교
천/개/오지영-한주성-미정/19:00/홍대/전도의장
번/노/장은지-장민준-미정/19:00 /홍대/
번/통/복서경-레랑-미정/18:00/홍대/:x:연락두절
우/통/배수연-김동우-미정/19:00/친교/:x:비합으로 내림
이/통/임광민-유태상-미정/19:30/홍대/전도의장/:o:
이/개/유안나-이종현-미정/20:00/홍대/전도의장/:o:
2) 따기타겟만남 (따기목표: 00명)
번/이수연-정선아-미정/20:00/전도의장/:o:
이/이동연-염현서-미정/19:00/에니어풀이/:o:
이/손승희-서승현-미정/19:00/인터뷰/:o:
이/유안나-정운수-미정/20:00/전도의장/(부재로 확티 필요)
이/유안나-서우진-미정/20:00/전도의장/(부재로 확티 필요)
이/이유진B-안상준-미정/20:00/전도의장/(부재로 다시 전화예정)
이/김반디-서나영-미정/19:30/전도의장/:o:
천/변준혁-신종민-미정/18:00/전도의장/:o:
천/오지영-한주성-미정/19:00/전도의장/
번/권은재-안민석-장은지/19:00/전도의 장
이/통/임광민-유태상-미정/19:30/홍대/전도의장/:o:
이/개/유안나-이종현-미정/20:00/홍대/전도의장/:o:
"""

text_2 = """
번-통/비/합/안민석-권은재/권은재/19:00, 합정/////
번-통/비/찾/레랑-복서경/복서경/18:00, 홍대/////
번-노/비/찾/정선아-이수연/이수연/20:00, 합정/////
번-통/비/찾/장민준-장은지/장은지/19:00, 합정/////
상-통/비/찾/박석훈-김유진/김유진/19:00, 홍대/////
상-노/비/찾/한윤성-엄채영/미정/, /////
상-통/비/찾/정승환-김상희/김상희/19:00, 홍대/////
상-통/비/찾/별사탕-강성용/아바타/19:00, 홍대/////
상-노/비/찾/오승욱-한창민/한창민/19:30, 홍대/////
우-통/비/찾/김동우-배수연/배수연/19:00, 홍대/////
우-통/비/따/이우주-배수연/배수연/19:20, 홍대/////
우-노/비/따/이수연-이인용/이인용,최혜연/20:00, 홍대/////
이-지/비/합/염현서-이동연/유안나/19:00, 응암/됨////
이-노/비/찾/서승현-손승희/김상헌/19:00, 홍대/됨////
이-노/비/찾/정운수-유안나//20:00, 홍대/안됨/세미나///
이-노/비/찾/서우진-유안나//20:00, 홍대/안됨/세미나///
이-노/비/찾/안상준-이유진B//20:00, 홍대/안됨/세미나///
이-노/비/찾/서나영-김반디//19:30, 홍대/됨/세미나///
이-통/비/찾/김봉주-이유진B//16:00, 홍대/됨////
이-통/비/찾/유태상-임광민(기연지)//19:30, 홍대/됨/세미나///
이-노/비/찾/이종현-유안나//20:00, 홍대/됨/세미나///
이-지/비/찾/이태로-정준호//19:00, 광명/안됨////
천-지/비/합/신종민-변준혁/변준혁/18:00, 홍대//세미나///
천-노/비/찾/한주성-오지영/오지영/19:00, 홍대//세미나///
"""

def set_text_1(_text_1):
    global text_1
    text_1 = _text_1

def get_text_1():
    return text_1

# 개, 찾, 합을 노로 변경하는 함수
def replace_keywords(line):
    line = line.replace('노', '개')
    line = line.replace('/비', '')
    line = line.replace('-미정', '')
    return line

# -를 /로, 이름 순서 변경, -미정 제거, 시간/홍대 형식 변경하는 함수
def format_line_text_1(line):
    parts = line.split('/')
    if('-' not in parts[1]):
        del parts[1]
    parts[1] = '/'.join([parts[1].split('-')[0], parts[1].split('-')[1]])
    return '/'.join(parts[:3]).strip()

# -를 /로, 이름 순서 변경, -미정 제거, 시간/홍대 형식 변경하는 함수
def format_line_text_2(line):
    parts = line.split('/')
    parts[0] = parts[0].split('-')[0]
    parts[2] = '/'.join(reversed(parts[2].split('-')))
    parts[4] = parts[4].split(', ')[0]
    del parts[3]
    del parts[1]
    return '/'.join(parts[:3]).strip()

# 형식 변경 함수 호출하여 2번 문자열 변환
def text_compare(text_1, text_2):
    del text_1[0]
    text_1 = '\n'.join([s for s in text_1 if '타겟만남' not in s])
    
    formatted_text_1 = ''
    for line in text_1.split('\n'):
        if line:
            line = replace_keywords(line)
            line = format_line_text_1(line)
            formatted_text_1 += line + '\n'
    formatted_text_1 = sorted(formatted_text_1.split('\n'))

    # 형식 변경 함수 호출하여 2번 문자열 변환
    formatted_text_2 = ''
    for line in text_2.split('\n'):
        if line:
            line = replace_keywords(line)
            line = format_line_text_2(line)
            formatted_text_2 += line + '\n'
    formatted_text_2 = sorted(formatted_text_2.split('\n'))

    result = list(set(formatted_text_1).symmetric_difference(set(formatted_text_2)))

    # 결과 출력
    # print("변환된 1번 문자열:\n", '\n'.join(list(set(formatted_text_1))))
    # print("변환된 2번 문자열:\n", '\n'.join(list(set(formatted_text_2))))

    print("최종 중복값 제거 리스트:\n", '\n'.join(sorted(result)))

    return '\n'.join(sorted(result))