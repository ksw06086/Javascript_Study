import asyncio
from crawler import *
from get_browser import CreateBrowser
from database.work_mysql import MySQLWork
from database.work_mongo import MongoWork

mysql_db = MySQLWork()
mongo_db = MongoWork()


async def get_keywords():
    return mysql_db.fetch_all_keywords()


async def open_page_and_crawl(browser, keyword):
    # 페이지 열기
    page = await browser.newPage()
    task = asyncio.create_task(movie_crwaler(page, keyword))
    return page, task


async def open_pages_with_delay(browser, movie_keywords):
    tasks = []
    for keyword in movie_keywords:
        page, task = await open_page_and_crawl(browser, keyword)
        tasks.append(task)
        await asyncio.sleep(1)
    return tasks


async def main():
    create_browser = CreateBrowser()
    browser = await create_browser.get_browser()
    # await async_browser(browser)

    keywords = await get_keywords()
    movie_keywords = [item[2] for item in keywords]
    print(movie_keywords)
    tasks = await open_pages_with_delay(browser, movie_keywords)
    await asyncio.gather(*tasks)

    await browser.close()

if __name__ == "__main__":
    asyncio.run(main())