from urllib import parse

import requests
from bs4 import BeautifulSoup


def get_page_url():
    page_url_list = []
    base_url = 'https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=pnt&tg=0&date=20200405&page='
    for i in range(1, 10 + 1):
        page_url_list.append(base_url + str(i))
    return page_url_list


def get_url(page_url):
    req = requests.get(page_url)
    soup = BeautifulSoup(req.text, 'html.parser')
    url_list = []

    for movie_list in soup.select('div.tit5'):
        url_list.append(movie_list.a['href'])
    return url_list


def get_item(url):
    base_url = "https://movie.naver.com"
    rating_list = ['전체 관람가', '12세 관람가', '15세 관람가', '청소년 관람불가']
    genre = []  # 장르
    pub_year = []  # 개봉연도
    actors = []  # 배우
    directors = []  # 감독

    soup = BeautifulSoup(requests.get(base_url + url).text, 'html.parser')
    try:
        title = soup.select_one('h3.h_movie').find('a').getText()  # 타이틀
    except AttributeError:
        return None
    b_sub_title = soup.select_one('strong.h_movie2').getText()
    title_english = (list(map(str.strip, b_sub_title.split(', ')))[0])
    d1 = soup.select_one('dl.info_spec')
    s1 = d1.dt.findNextSibling('dd')
    temp = s1.find_all('a')
    temp2 = s1.find_all('span')

    movie_length = temp2[2].getText().strip()  # 상영시간

    for a in temp:
        p1 = parse.urlparse(a['href'])
        if 'genre' in p1[4]:
            if int(p1.query[6:]) > 28:
                return None
            genre.append(p1.query[6:])  # 장르

        if 'open' in p1[4] and not pub_year:
            pub_year = p1[4][5:9]  # 개봉연도
    s2 = s1.findNextSibling('dd')
    s3 = s2.findNextSibling('dd')
    s4 = s3.findNextSibling('dd')
    for a in s2.p.select('a'):
        directors.append(a.getText())  # 감독

    for a in s3.p.select('a'):
        actors.append(a.getText())

    try:
        rating = s4.a.getText()  # 관람등급
        if rating not in rating_list:
            return None
    except AttributeError:
        return None
    image_thumb_url = soup.select_one('div.poster').find('a').img['src']  # 포스터 url
    image_url = parse.urlunsplit(parse.urlsplit(image_thumbnail_url)._replace(query=''))
    summary_text = soup.select("div.obj_section > div.video > div.story_area > p.con_tx")
    if summary_text:
        summary = summary_text[0].get_text(strip=True)  # 줄거리
    else:
        summary = ''
    return {
        'title': title,
        'title_english': title_english,
        'genre': genre,
        'pub_year': pub_year,
        'length': movie_length,
        'rating': rating,
        'actor': actors,
        'director': directors,
        'image_thumb_url': image_thumb_url,
        'image_url': image_url,
        'summary': summary
    }
