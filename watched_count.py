import requests
from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import Error
from pprint import pprint
from datetime import datetime, timedelta
import env

yesterday = datetime.now() - timedelta(days=1)
formatted_yesterday = yesterday.strftime('%Y%m%d')    

# API에서 박스오피스 데이터 가져오기
def fetch_box_office_data(api_url, search_movie, search_date):
    #* 1 : 순위 / 2 : 영화명(select('span')[0] - 제목, select('span')[1] - 증감) / 3 : 개봉일 / 4 : 매출액 / 5 : 매출액점유율 / 6 : 매출액증감(전일대비) / 
    #* 7 : 누적매출액 / 8 : 관객수 / 9 : 관객수증감(전일대비) / 10 : 누적관객수 / 11 : 스크린 수 / 12 : 상영횟수
    data = {
        'loadEnd' : '0',
        'searchType' : 'search',
        'sSearchFrom': search_date, 
        'sSearchTo' : search_date
    }
    response = requests.post(api_url, data=data)
    soup = BeautifulSoup(response.content, "html.parser")
    trs = soup.select('table tbody tr')
    insert_data = {}
    for tr in trs:
        if search_movie.replace(' ', '') in tr.select('td:nth-child(2) span')[0].getText().replace(' ','').strip():
            insert_data['title'] = search_movie
            insert_data['watched_count'] = int(tr.select('td:nth-child(10)')[0].getText().replace(',', '').strip())
            break
    return insert_data

# MySQL 데이터베이스에 데이터 삽입
def insert_data_to_mysql(db_config, data):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # INSERT 쿼리
        query = "INSERT INTO movie_rank (spot, spot_inten, spot_state, code, title, open_date, sales_amt, sales_inten, sales_acc, watched_count, watched_inten, watched_acc, screen_count, show_count, spot_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        for item in data['boxOfficeResult']['dailyBoxOfficeList']:
            pprint(item)
            cursor.execute(query, (item['rank'], item['rankInten'], item['rankOldAndNew'], item['movieCd'], item['movieNm'], item['openDt'], int(item['salesAmt']), int(item['salesInten']), int(item['salesAcc']), int(item['audiCnt']), int(item['audiInten']), int(item['audiAcc']), int(item['scrnCnt']), int(item['showCnt']), yesterday.date()))

        conn.commit()
    except Error as e:
        print(f"Error: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# 메인 함수
def main():
    api_url = f"https://www.kobis.or.kr/kobis/business/stat/boxs/findDailyBoxOfficeList.do"
    data = fetch_box_office_data(api_url, '서울의 봄', '2023-11-20')
    pprint(data)

    if data:
        db_config = {
            'host': env.HOSTNAME,
            'user': env.USERNAME,
            'password': env.PASSWORD,
            'database': env.DATABASE
        }
        # insert_data_to_mysql(db_config, data)

if __name__ == '__main__':
    main()