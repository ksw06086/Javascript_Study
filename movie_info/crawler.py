import asyncio
from bs4 import BeautifulSoup


async def get_soup(page):
    content = await page.content()
    return BeautifulSoup(content, 'html.parser')


async def extract_info(page, search_text):
    try:
        info_groups = await page.xpath("//div[@class='info_group']")
        if not info_groups:
            print(f"No 'info_group' elements found.")
            return None

        for info_group in info_groups:
            dt_elements = await info_group.xpath(".//dt")
            for dt_element in dt_elements:
                dt_text = await page.evaluate('element => element.textContent.trim()', dt_element)
                if search_text in dt_text:
                    sibling_dd_texts = await page.evaluate('''dt => {
                        const sibling_dds = [];
                        let nextSibling = dt.nextElementSibling;
                        while (nextSibling) {
                            if (nextSibling.tagName === 'DD') {
                                sibling_dds.push(nextSibling.textContent.trim());
                            }
                            nextSibling = nextSibling.nextElementSibling;
                        }
                        return sibling_dds;
                    }''', dt_element)
                    if sibling_dd_texts:
                        return sibling_dd_texts[0]
        print(f"No '{search_text}' elements found.")
        return None

    except Exception as e:
        print("Error while finding elements:", e)
        return None


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


async def get_director(page, movie):
    try:
        search_url = f"https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&ssc=tab.nx.all&query=영화+{movie}+감독"
        await page.goto(search_url, {"waitUntil": "domcontentloaded"})
        await asyncio.sleep(3)
        director_soup = await get_soup(page)
        return await get_soup_select(director_soup, 'div.title_box strong.name')
    except Exception as e:
        print(f"Error in get_director: {e}")
        return []


async def get_actor(page, movie):
    try:
        search_url = f"https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&ssc=tab.nx.all&query=영화+{movie}+주연"
        await page.goto(search_url, {"waitUntil": "domcontentloaded"})
        await asyncio.sleep(3)
        actor_soup = await get_soup(page)
        return await get_soup_select(actor_soup, 'div.list_image_info._panel_wrapper div.title_box > strong > a')
    except Exception as e:
        print(f"Error in get_actor: {e}")
        return []


async def get_grade(page, movie):
    try:
        search_url = f"https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&ssc=tab.nx.all&query=영화+{movie}+관람평"
        await page.goto(search_url, {"waitUntil": "domcontentloaded"})
        await asyncio.sleep(3)
        grade_soup = await get_soup(page)
        grade_info = grade_soup.select_one('div.list_info ul.list')

        # Extract grade, male ratio, and female ratio with appropriate handling if grade_info is None
        grade = await get_soup_select_one(grade_info, 'span.area_star_number') if grade_info else None
        male_ratio = await get_soup_select_one(grade_info, 'li.type_male span.ratio') if grade_info else None
        female_ratio = await get_soup_select_one(grade_info, 'li.type_female span.ratio') if grade_info else None

        return grade, male_ratio, female_ratio
    except Exception as e:
        print(f"Error in get_grade: {e}")
        return None, None, None


async def movie_crwaler(page, movie):
    search_url = f"https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&ssc=tab.nx.all&query=영화+{movie}+정보"
    await page.goto(search_url, {"waitUntil": "domcontentloaded"})
    await asyncio.sleep(3)
    info_soup = await get_soup(page)
    summary_text = await get_soup_select_one(info_soup, 'div.intro_box._content > p')

    genre_info = await extract_info(page, '장르')
    movie_rating = await extract_info(page, '등급')
    country_info = await extract_info(page, '국가')
    runtime_info = await extract_info(page, '러닝타임')
    distributor_info = await extract_info(page, '배급')
    image_url = await get_soup_select_one(info_soup, 'div.detail_info img', 'src')
    director_name = await get_director(page, movie)
    if len(director_name) > 1:
        director_name = ', '.join(director_name)
    actor_list = await get_actor(page, movie)
    actor_string = ', '.join(actor_list)
    grade, male_ratio, female_ratio = await get_grade(page, movie)

    movie_dict = {
        'genre': genre_info,
        'rating': movie_rating,
        'country': country_info,
        'runtime': runtime_info,
        'distributor': distributor_info,
        'image_url': image_url,
        'director': director_name,
        'actor': actor_string,
        'grade': grade,
        'male_ratio': male_ratio,
        'female_ratio': female_ratio,
        'summary': summary_text,
    }
    print(movie_dict)
    return movie_dict








