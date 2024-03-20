import requests
import mysql.connector
from mysql.connector import Error
from pprint import pprint
from datetime import datetime, timedelta
import env

yesterday = datetime.now() - timedelta(days=1)
formatted_yesterday = yesterday.strftime('%Y%m%d')    

# API에서 박스오피스 데이터 가져오기
def fetch_box_office_data(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()  # JSON 데이터 반환
    else:
        return None

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
    api_url = f"http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?key=827c670f8f542206ff408e07ea616ebb&targetDt={formatted_yesterday}"
    data = fetch_box_office_data(api_url)

    if data:
        db_config = {
            'host': env.HOSTNAME,
            'user': env.USERNAME,
            'password': env.PASSWORD,
            'database': env.DATABASE
        }
        insert_data_to_mysql(db_config, data)

if __name__ == '__main__':
    main()