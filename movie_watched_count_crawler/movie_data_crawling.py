import requests, re, asyncio, os
from bs4 import BeautifulSoup
from lxml import etree
from get_browser import CreateBrowser
import mysql.connector
from mysql.connector import Error
from pprint import pprint
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

yesterday = datetime.now() - timedelta(days=1)
formatted_yesterday = yesterday.strftime('%Y%m%d')   

# API에서 박스오피스 영화 코드 가져오기
async def fetch_box_office_movie_code(title, open_date):
    data = {
        'CSRFToken': 'HiO-Pq73Tiv9PlN4Onk7_RFUHKY5o1HYAjRnhBWebHI',
        'curPage': 1,
        'searchType': 'undefined',
        'point': '',
        'orderBy': '',
        'sMovName': title,
        'sDirector': '',
        'sPrdtYearS': '',
        'sPrdtYearE': '',
        'sOpenYearS': open_date.strftime('%Y-%m-%d'),
        'sOpenYearE': open_date.strftime('%Y-%m-%d')
    }
    api_url = f"https://www.kobis.or.kr/kobis/business/mast/mvie/searchMovieList.do"
    response = requests.post(api_url, data=data)
    soup = BeautifulSoup(response.content, "html.parser")
    movie_code = soup.select_one('table tbody tr td.tac')
    if movie_code:
        return movie_code.text.strip()
    else:
        return None

# API에서 박스오피스 영화 누적관객수 가져오기
async def fetch_box_office_watched_count(movie_code):
    # 이전에 상영된 영화도 개봉일 10일 후까지의 누적관객수 데이터는 가져올 수 있음
    # 이전에 상여된 영화도 최신 10일의 누적관객수 데이터는 가져올 수 있음
    data = {
        'code': movie_code,
        'sType': 'stat',
        'CSRFToken': 'HiO-Pq73Tiv9PlN4Onk7_RFUHKY5o1HYAjRnhBWebHI'
    }
    api_url = f"https://www.kobis.or.kr/kobis/business/mast/mvie/searchMovieDtl.do"
    response = requests.post(api_url, data=data)
    soup = BeautifulSoup(response.content, "lxml")
    dom = etree.HTML(str(soup))
    all_watched_count = dom.xpath('//caption[text()="KOBIS통계"]/following-sibling::tbody//td[text()="전국"]/following-sibling::td[last()]')
    if all_watched_count:
        return re.sub(r'[^\d]', '', all_watched_count[0].text)
    else:
        return None

# MySQL 데이터베이스에 영화 제목 조회
def get_movie_titles_and_open_dates(db_config):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # SELECT 쿼리
        query = """
            SELECT title, open_date
            FROM movie
            WHERE NOW() BETWEEN start_date and end_date
            """
        cursor.execute(query)
        return [{'title': data[0], 'open_date': data[1]} for data in cursor.fetchall()]
    except Error as e:
        print(f"Error: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# MySQL 데이터베이스에 영화 movie_info 데이터 삽입
def insert_data_to_mysql(db_config, title, open_date, all_watched_count):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # INSERT 쿼리
        query = "INSERT INTO movie_info (title, open_date, watched_count, created_at) "\
            "VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (title, open_date, all_watched_count, datetime.now()))

        conn.commit()
    except Error as e:
        print(f"Error: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# 메인 함수
async def main():
    # create_browser = CreateBrowser()
    # browser = await create_browser.get_browser()

    db_config = {
        'host': os.getenv("HOSTNAME"),
        'port': 3310,
        'user': 'unionMaster',
        'password': os.getenv("PASSWORD"),
        'database': os.getenv("DATABASE")
    }
    movies = get_movie_titles_and_open_dates(db_config)
    for movie in movies:
        movie_code = await fetch_box_office_movie_code(movie['title'], movie['open_date'])
        if movie_code:
            print(f"{movie['title']} : {movie_code}")
            all_watched_count = await fetch_box_office_watched_count(movie_code)
            if all_watched_count:
                insert_data_to_mysql(db_config, movie['title'], movie['open_date'], all_watched_count)
                print(f"{movie['title']} 관객수 : {all_watched_count}")
                print(f"{movie['title']} INSERT COMPLETE")
            else:
                print(f"Error: {movie['title']} - {movie['open_date']} None All Watched Count")
        else:
            print(f"Error: {movie['title']} - {movie['open_date']} None Movie Code")
        print()

    # await browser.close()
    

if __name__ == '__main__':
    asyncio.run(main())