from urllib import parse

from bs4 import BeautifulSoup
import requests
import urllib.request

url_list = []
title_list = []
base_url = 'https://movie.naver.com'
movie_url = []

# base_url + url_list[0]


# 네이버영화의 랭킹순위에서 각 영화들의 url을 가져옴
def get_url():
    url = 'https://movie.naver.com/movie/sdb/rank/rmovie.nhn'
    req = requests.get(url)
    soup = BeautifulSoup(req.text)

    for title in soup.select('div.tit3'):
        title_list.append(title.a.gettext().strip())
        url_list.append(title.a['href'])


def get_item():
    title = []  # 타이틀
    genre = []  # 장르
    pub_year = []  # 개봉연도
    movie_length = []  # 상영시간
    actor = []  # 배우
    rating = []  # 관람등급
    director = []  # 감독
    image_url = []  # 포스터 url
    # 줄거리

    url = base_url + url_list[0]
    soup = BeautifulSoup(requests.get(url).text)
    title.append(soup.select_one('h3.h_movie').find('a').getText())  # 타이틀
    d1 = soup.select_one('dl.info_spec')
    s1 = d1.dt.findNextSibling('dd')
    temp = s1.find_all('a')
    temp2 = s1.find_all('span')
    genre_dict = {
        '1': '드라마', '2': '판타지', '3': '서부', '4': '공포', '5': '로맨스', '6': '모험', '7': '스릴러',
        '8': '느와르', '9': '컬트', '10': '다큐멘터리', '11': '코미디', '12': '가족', '13': '미스터리',
        '14': '전쟁', '15': '애니메이션', '16': '범죄', '17': '뮤지컬', '18': 'SF', '19': '액션',
        '20': '무협', '21': '에로', '22': '서스펜스', '23': '서사', '24': '블랙코미디', '25': '실험',
        '26': '영화카툰', '27': '영화음악', '28': '영화패러디포스터'
    }

    movie_length.append(temp2[2].getText().strip())  # 상영시간

    for a in temp:
        p1 = parse.urlparse(a['href'])
        if 'genre' in p1[4]:
            genre.append(genre_dict[p1.query[6:]])  # 장르

        if 'open' in p1[4] and not pub_year:
            pub_year.append(p1[4][5:9])  # 개봉연도

    s2 = s1.findNextSibling('dd')
    s3 = s2.findNextSibling('dd')
    s4 = s3.findNextSibling('dd')
    director.append(s2.a.getText())  # 감독
    actor.append(s3.a.getText())  # 배우
    rating.append(s4.a.getText())  # 관람등급
    image_url.append(soup.select_one('div.poster').find('a').img['src'])  # 포스터 url


"""
    return : dict
    {
        'title': title,
        'genre' : gendre
    }
"""
