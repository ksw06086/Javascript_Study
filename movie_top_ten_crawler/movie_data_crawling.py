import requests, re, asyncio, os
from bs4 import BeautifulSoup
from get_browser import CreateBrowser
import mysql.connector
from mysql.connector import Error
from pprint import pprint
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

yesterday = datetime.now() - timedelta(days=1)
formatted_yesterday = yesterday.strftime('%Y%m%d')   

# Naver에서 별점, 남성비, 여성비 데이터 가져오기
async def find_naver_rate_data(browser, title):
    # 페이지 열기
    page = await browser.newPage()
    search_url = f"https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&ssc=tab.nx.all&query=영화+{title}+정보"
    await page.goto(search_url, {"waitUntil": "domcontentloaded"})
    await asyncio.sleep(5)
    content = await page.content()
    info_soup = BeautifulSoup(content, 'html.parser')
    summary_text = await get_soup_select_one(info_soup, 'div.intro_box._content > p')
    rate, male_ratio, female_ratio = await get_rate(page, title)
    director_name = await get_director(page, title)
    # genre_info = await extract_info(page, '장르') // extract_info는 movie_info의 crawler에 있음
    # movie_rating = await extract_info(page, '등급')
    # country_info = await extract_info(page, '국가')
    # runtime_info = await extract_info(page, '러닝타임')
    # distributor_info = await extract_info(page, '배급')
    # image_url = await get_soup_select_one(info_soup, 'div.detail_info img', 'src')
    # actor_list = await get_actor(page, movie) // get_director는 movie_info의 crawler에 있음
    # actor_string = ', '.join(actor_list)
    await page.close()

    return summary_text, rate, male_ratio, female_ratio, director_name

# Naver에서 선택자에 맞추어서 1개의 데이터만 가져오기
async def get_soup_select_one(soup, selector, attribute=None):
    try:
        element = soup.select_one(selector)
        if element:
            if attribute:
                return element.get(attribute, None)
            else:
                return element.text.strip()
        return None
    except Exception as e:
        print(f"Error in get_soup_select_one: {e}")
        return None

# Naver에서 선택자에 맞추어서 데이터 리스트 가져오기
async def get_soup_select(soup, selector, attribute=None):
    try:
        elements = soup.select(selector)
        results = []
        for element in elements:
            if attribute:
                results.append(element.get(attribute, None))
            else:
                results.append(element.text.strip())
        return results
    except Exception as e:
        print(f"Error in get_soup_select: {e}")
        return []
    
# Naver에서 별점, 남녀성비 가져오기
async def get_rate(page, movie):
    try:
        search_url = f"https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&ssc=tab.nx.all&query=영화+{movie}+관람평"
        await page.goto(search_url, {"waitUntil": "domcontentloaded"})
        await asyncio.sleep(5)
        content = await page.content()
        rate_soup = BeautifulSoup(content, 'html.parser')
        rate_info = rate_soup.select_one('div.list_info ul.list')

        # Extract grade, male ratio, and female ratio with appropriate handling if grade_info is None
        rate = await get_soup_select_one(rate_info, 'span.area_star_number') if rate_info else None
        male_ratio = await get_soup_select_one(rate_info, 'li.type_male span.ratio') if rate_info else None
        female_ratio = await get_soup_select_one(rate_info, 'li.type_female span.ratio') if rate_info else None

        return rate, male_ratio, female_ratio
    except Exception as e:
        print(f"Error in get_rate: {e}")
        return None, None, None

# Naver에서 감독 데이터 가져오기
async def get_director(page, movie):
    try:
        search_url = f"https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&ssc=tab.nx.all&query=영화+{movie}+감독"
        await page.goto(search_url, {"waitUntil": "domcontentloaded"})
        await asyncio.sleep(3)
        content = await page.content()
        director_soup = BeautifulSoup(content, 'html.parser')
        return await get_soup_select(director_soup, 'div.title_box strong.name')
    except Exception as e:
        print(f"Error in get_director: {e}")
        return ['unknown']

# API에서 박스오피스 감독 데이터 가져오기
def fetch_box_office_staff_data(code):
    # data = {
    #     'movieCd' : code,
    #     'mgmtMore': 'N',
    #     'CSRFToken': 'fPrwiqvm7EXGb-NiYLbIukXnLntZrhFxHaTcAQTx6W8'
    # }
    # api_url = f"https://www.kobis.or.kr/kobis/business/mast/mvie/searchMovStaffLists.do"
    # response = requests.post(api_url, headers={'Accept': 'application/json, text/javascript, */*; q=0.01'}, data=data)
    # staffs = response.json()
    # staff_dics = {'감독': []}
    # for staff in staffs:
    #     if staff_dics.get(staff['roleNm']):
    #         staff_dics[staff['roleNm']].append(staff['peopleNm'])
    #     else:
    #         staff_dics[staff['roleNm']] = [staff['peopleNm']]

    # return staff_dics
    return None

# API에서 박스오피스 배우 데이터 가져오기
def fetch_box_office_actor_data(code):
    data = {
        'movieCd' : code,
        'CSRFToken': 'fPrwiqvm7EXGb-NiYLbIukXnLntZrhFxHaTcAQTx6W8'
    }
    api_url = f"https://www.kobis.or.kr/kobis/business/mast/mvie/searchMovActorLists.do"
    response = requests.post(api_url, headers={'Accept': 'application/json, text/javascript, */*; q=0.01'}, data=data)
    actors = response.json()
    main_actor = []
    sub_actor = []
    for actor in actors:
        if '1' in actor['actorGb']: main_actor.append(actor['actorNm'])
        if '5' in actor['actorGb']: sub_actor.append(actor['actorNm'])

    return main_actor, sub_actor 

# API에서 박스오피스 포스터 URL, 국가 데이터 가져오기
def fetch_box_office_detail_data(code):
    data = {
        'code' : code,
        'sType' : '',
        'titleYN' : 'Y',
        'etcParam': '', 
        'isOuterReq' : 'false',
        'CSRFToken': 'fPrwiqvm7EXGb-NiYLbIukXnLntZrhFxHaTcAQTx6W8'
    }
    api_url = f"https://www.kobis.or.kr/kobis/business/mast/mvie/searchMovieDtl.do"
    response = requests.post(api_url, data=data)
    soup = BeautifulSoup(response.content, "html.parser")
    image_url = f"https://www.kobis.or.kr{soup.select_one('div.ovf.info a')['href'].strip()}"
    movie_info = re.sub(r'[\s]+', '', soup.select_one('dl.ovf.cont dd:nth-child(8)').getText())

    return image_url, movie_info

# API에서 박스오피스 예매율 데이터 가져오기
def fetch_box_office_real_ticket_data():
    data = {
        'CSRFToken': 'fPrwiqvm7EXGb-NiYLbIukXnLntZrhFxHaTcAQTx6W8',
        'loadEnd': '0',
        'repNationCd': '',
        'areaCd': '',
        'repNationSelected': '',
        'totIssuAmtRatioOrder': '',
        'totIssuAmtOrder': '',
        'addTotIssuAmtOrder': '',
        'totIssuCntOrder': '',
        'totIssuCntRatioOrder': '',
        'addTotIssuCntOrder': '',
        'dmlMode': 'search',
        'allMovieYn': 'Y',
        'sMultiChk': ''
    }
    api_url = f"https://www.kobis.or.kr/kobis/business/stat/boxs/findRealTicketList.do"
    response = requests.post(api_url, data=data)
    soup = BeautifulSoup(response.content, "html.parser")
    trs = soup.select('table tbody tr')

    return trs

# 예매율 데이터 찾아서 보내주기
def find_box_office_real_ticket_data(real_ticket_trs, title):
    for tr in real_ticket_trs:
        ticket_movie_title = tr.select_one('td:nth-child(2) span').getText().replace(' ','').strip()
        if title == ticket_movie_title:
            ticketing_percent = tr.select_one('td:nth-child(4)').getText().replace(' ','').strip()
            ticketing_count = tr.select_one('td:nth-child(7)').getText().replace(' ','').strip()
            return ticketing_percent, ticketing_count
    return None, None

# API에서 박스오피스 데이터 가져오기
async def fetch_box_office_data(browser, search_date, real_ticket_trs):
    #* 1 : 순위 / 2 : 영화명(select('span')[0] - 제목, select('span')[1] - 증감) / 3 : 개봉일 / 4 : 매출액 / 5 : 매출액점유율 / 6 : 매출액증감(전일대비) / 
    #* 7 : 누적매출액 / 8 : 관객수 / 9 : 관객수증감(전일대비) / 10 : 누적관객수 / 11 : 스크린 수 / 12 : 상영횟수
    data = {
        'CSRToken' : 'fPrwiqvm7EXGb-NiYLbIukXnLntZrhFxHaTcAQTx6W8',
        'loadEnd' : '0',
        'searchType' : 'search',
        'sSearchFrom': search_date, 
        'sSearchTo' : search_date,
        'sMultiMovieYn': '',
        'sRepNationCd': '',
        'sWideAreaCd': ''
    }
    api_url = f"https://www.kobis.or.kr/kobis/business/stat/boxs/findDailyBoxOfficeList.do"
    response = requests.post(api_url, data=data)
    soup = BeautifulSoup(response.content, "html.parser")
    trs = soup.select('table tbody tr')
    data_list = []
    for tr in trs[:10]:
        movie_code = re.findall(r'\d+', tr.select_one('td:nth-child(2) a')['onclick'])[0]
        image_url, movie_info = fetch_box_office_detail_data(movie_code)
        main_actors, sub_actors = fetch_box_office_actor_data(movie_code)
        
        grade = tr.select('td:nth-child(1)')[0].getText().replace(' ','').strip()
        title = tr.select('td:nth-child(2) span')[0].getText().replace(' ','').strip()
        ticketing_percent, ticketing_count = find_box_office_real_ticket_data(real_ticket_trs, title)
        summary_text, rate, male_ratio, female_ratio, director_name = await find_naver_rate_data(browser, title)
        # directors = fetch_box_office_staff_data(movie_code).get('감독') // 영화진흥원에는 없는데 네이버에 있는 경우가 있어 네이버로 갈아탐

        up_down = tr.select('td:nth-child(2) span')[1].getText().replace(' ','').strip()
        open_date = tr.select('td:nth-child(3)')[0].getText().replace(',', '').strip()
        watched_count = int(tr.select('td:nth-child(8)')[0].getText().replace(',', '').strip())
        watched_total_count = int(tr.select('td:nth-child(10)')[0].getText().replace(',', '').strip())
        screen_count = int(tr.select('td:nth-child(11)')[0].getText().replace(',', '').strip())
        show_count = int(tr.select('td:nth-child(12)')[0].getText().replace(',', '').strip())

        data_list.append({
            'grade' : grade,
            'movie_code': movie_code,
            'title': title,
            'up_down': up_down,
            'open_date': open_date, 
            'image_url': image_url,
            'movie_info': movie_info,
            'watched_count': watched_count, 
            'watched_total_count': watched_total_count,
            'screen_count': screen_count,
            'show_count': show_count,
            'main_actors': ','.join(main_actors),
            'sub_actors': ','.join(sub_actors),
            'directors': ','.join(director_name),
            'ticketing_percent': ticketing_percent,
            'ticketing_count': ticketing_count,
            'summary_text': summary_text,
            'rate': rate,
            'male_ratio': male_ratio,
            'female_ratio': female_ratio
        })
    return data_list

# MySQL 데이터베이스에 영화 제목 조회
def get_movie_titles(db_config):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # SELECT 쿼리
        query = """
            SELECT title
            FROM movie
            """
        cursor.execute(query)
        return [title[0] for title in cursor.fetchall()]
    except Error as e:
        print(f"Error: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# MySQL 데이터베이스에 필수 키워드 데이터 삽입
def insert_essential_keyword_to_mysql(db_config, data, keyword_idx):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # INSERT 쿼리
        query = "INSERT INTO essential_keyword (keyword_idx, keyword, created_at) "\
            "VALUES (%s, %s, %s)"
        cursor.execute(query, (
            int(keyword_idx),
            data['title'],
            datetime.now()
        ))

        conn.commit()
    except Error as e:
        print(f"Error: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# MySQL 데이터베이스에 키워드 데이터 삽입
def insert_keyword_to_mysql(db_config, data):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # INSERT 쿼리
        query = "INSERT INTO keyword (movie, cp_id, keyword, created_at) "\
            "VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (
            data['title'], 
            "경쟁작",
            data['title'], 
            datetime.now()
        ))

        conn.commit()

        # 동일 세션 내에서 바로 데이터 조회
        cursor.execute("SELECT idx FROM keyword ORDER BY idx DESC LIMIT 1")
        
        return cursor.fetchone()[0]
    except Error as e:
        print(f"Error: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# MySQL 데이터베이스에 영화 데이터 삽입
def insert_movie_to_mysql(db_config, data):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # INSERT 쿼리
        query = "INSERT INTO movie (title, member_id, open_date, director, producer, characters, poster, grade, genre, running_time, start_date, end_date, tag) "\
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (
            data['title'], 
            "경쟁작",
            data['open_date'], 
            data['directors'], 
            "경쟁작",
            data['main_actors'], 
            data['image_url'], 
            data['movie_info'].split('|')[4],
            data['movie_info'].split('|')[2],
            data['movie_info'].split('|')[3],
            datetime.now(),
            datetime.now() + timedelta(days=31),
            f"#{data['title']}"
        ))

        conn.commit()
    except Error as e:
        print(f"Error: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# MySQL 데이터베이스에 영화 Top 10 데이터 삽입
def insert_data_to_mysql(db_config, data_list):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # INSERT 쿼리
        query = "INSERT INTO movie_top_ten (grade, movie_code, movie_info, title, up_down, open_date, image_url, watched_count, watched_total_count, screen_count, show_count, main_actors, sub_actors, directors, ticketing_percent, ticketing_count, summary_text, search_date, rate, male_ratio, female_ratio, competitor_title) "\
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        for item in data_list:
            competitor_title = ""
            if item['grade'] == '1':
                competitor_title = data_list[1]['title']
            else:
                competitor_title = data_list[0]['title']    
            cursor.execute(query, (
                item['grade'], 
                item['movie_code'],
                item['movie_info'],  
                item['title'], 
                item['up_down'], 
                item['open_date'], 
                item['image_url'], 
                int(item['watched_count']), 
                int(item['watched_total_count']), 
                int(item['screen_count']), 
                int(item['show_count']), 
                item['main_actors'], 
                item['sub_actors'], 
                item['directors'], 
                item['ticketing_percent'] if item['ticketing_percent'] else '0.0%', 
                int(item['ticketing_count'].replace(",", "")) if item['ticketing_count'] else 0, 
                item['summary_text'], 
                yesterday.date(),
                item['rate'], 
                item['male_ratio'], 
                item['female_ratio'], 
                competitor_title
            ))

        conn.commit()
    except Error as e:
        print(f"Error: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# 메인 함수
async def main():
    create_browser = CreateBrowser()
    browser = await create_browser.get_browser()

    db_config = {
            'host': os.getenv("HOSTNAME"),
            'port': 3310,
            'user': os.getenv("USERNAME"),
            'password': os.getenv("PASSWORD"),
            'database': os.getenv("DATABASE")
        }
    real_ticket_trs = fetch_box_office_real_ticket_data()
    data_list = await fetch_box_office_data(browser, formatted_yesterday, real_ticket_trs)
    pprint(data_list)
    
    if data_list:
        insert_data_to_mysql(db_config, data_list)

        movies = get_movie_titles(db_config)
        for data in data_list:
            if data['title'] not in movies:
                insert_movie_to_mysql(db_config, data)
                keyword_idx = insert_keyword_to_mysql(db_config, data)
                insert_essential_keyword_to_mysql(db_config, data, keyword_idx)

    await browser.close()
    

if __name__ == '__main__':
    asyncio.run(main())