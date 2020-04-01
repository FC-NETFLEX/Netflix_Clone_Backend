from urllib import parse
from bs4 import BeautifulSoup
import requests
import magic

def get_url():
    url = r'https://movie.naver.com/movie/sdb/rank/rmovie.nhn'
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    url_list = []

    for movie_list in soup.select('div.tit3'):
        url_list.append('https://movie.naver.com' + movie_list.a['href'])
    return url_list


def get_item(movie_url):
    genre = []  # 장음르
    pub_year = '정보없'  # 개봉연도
    actors = []  # 배우
    directors = []  # 감독

    url = movie_url
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    title = soup.select_one('h3.h_movie').find('a').getText()  # 타이틀
    b_sub_title = soup.select_one('strong.h_movie2').getText()
    title_english = (list(map(str.strip, b_sub_title.split(', ')))[0])  # 서브타이틀 / 영어제목
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

    movie_length = temp2[2].getText().strip()  # 상영시간

    for a in temp:
        p1 = parse.urlparse(a['href'])
        if 'genre' in p1[4]:
            genre.append(genre_dict[p1.query[6:]])  # 장르

        if 'open' in p1[4]:
            pub_year = p1[4][5:9]  # 개봉연도

    s2 = s1.findNextSibling('dd')
    s3 = s2.findNextSibling('dd')
    s4 = s3.findNextSibling('dd')
    for a in s2.p.select('a'):
        directors.append(a.getText())
    for a in s3.p.select('a'):
        actors.append(a.getText())
    try:
        rating = s4.a.getText()  # 관람등급
    except AttributeError:
        rating = '전체 관람가'
    image_url = soup.select_one('div.poster').find('a').img['src']  # 포스터 url
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
        'image_url': image_url,
        'summary': summary
    }

