from django.shortcuts import render,get_object_or_404
from bs4 import BeautifulSoup
from decouple import config
import requests
from urllib.request import urlopen
from pprint import pprint
from IPython import embed
response = {'display': 5,
 'items': [{'actor': '휴 잭맨|조 샐다나|자흐 갈리피아나키스|엠마 톰슨|',
            'director': '크리스 버틀러|',
            'image': 'https://ssl.pstatic.net/imgmovie/mdi/mit110/1816/181692_P21_144315.jpg',
            'link': 'https://movie.naver.com/movie/bi/mi/basic.nhn?code=181692',
            'pubDate': '2019',
            'subtitle': 'Missing Link',
            'title': '<b>잃어버린 세계를 찾아서</b>',
            'userRating': '8.34'},
           {'actor': '드웨인 존슨|조쉬 허처슨|마이클 케인|바네사 허진스|',
            'director': '브래드 페이튼|',
            'image': 'https://ssl.pstatic.net/imgmovie/mdi/mit110/0810/81010_P22_120221.jpg',
            'link': 'https://movie.naver.com/movie/bi/mi/basic.nhn?code=81010',
            'pubDate': '2011',
            'subtitle': 'Journey 2: The Mysterious Island',
            'title': '<b>잃어버린 세계를 찾아서</b> 2 : 신비의 섬',
            'userRating': '7.11'},
           {'actor': '브렌든 프레이저|조쉬 허처슨|',
            'director': '에릭 브레빅|',
            'image': 'https://ssl.pstatic.net/imgmovie/mdi/mit110/0614/F1433-01.jpg',
            'link': 'https://movie.naver.com/movie/bi/mi/basic.nhn?code=61433',
            'pubDate': '2008',
            'subtitle': 'Journey To The Center Of The Earth 3D',
            'title': '<b>잃어버린 세계를 찾아서</b>',
            'userRating': '7.84'},
           {'actor': '릭 슈로더|빅토리아 프랫|',
            'director': 'T.J. 스콧|',
            'image': 'https://ssl.pstatic.net/imgmovie/mdi/mit110/0739/73952_P03_131847.jpg',
            'link': 'https://movie.naver.com/movie/bi/mi/basic.nhn?code=73952',
            'pubDate': '2008',
            'subtitle': 'Journey To The Center Of The Earth',
            'title': '<b>잃어버린 세계를 찾아서</b> 2 : 지구 속 여행',
            'userRating': '6.00'},
           {'actor': '돈 프랭크스|',
            'director': '로라 세퍼드|',
            'image': '',
            'link': 'https://movie.naver.com/movie/bi/mi/basic.nhn?code=78512',
            'pubDate': '1996',
            'subtitle': 'Journey To The Center Of The Earth',
            'title': '<b>잃어버린 세계를 찾아서</b>',
            'userRating': '0.00'}],
    'lastBuildDate': 'Fri, 22 Nov 2019 23:12:45 +0900',
    'start': 1,
    'total': 5}

actors =  list(filter(lambda x: x != "", response['items'][0]['actor'].split('|')))
html = urlopen('https://movie.naver.com/movie/bi/mi/basic.nhn?code=181692')
source = html.read()
html.close()
soup = BeautifulSoup(source,'html.parser')
div = soup.find('div','people')
iag_alt = div.find_all('img')
# pprint(div)

ac_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json'
key = config('API_KEY')
url = f'{ac_url}?key={key}&peopleNm=이병헌'
response = requests.get(url)
data = response.json()
pprint(data['peopleListResult']['totCnt'])  # totCnt == 1이냐 아니냐
if data['peopleListResult']['totCnt'] == 1:
    pass
elif data['peopleListResult']['totCnt'] >1:
    filmos = list(filter(lambda x: x != "", data['peopleListResult']['peopleList'][0]['filmoNames'].split('|'))) 
    print(filmos)
    pass



# for d in iag_alt:
#     print(d.attrs['alt'])
#     print(d.attrs['src'])
# print(actors)
# embed()
# actor = Actor()
# genre = Genre.objects.filter(genreNm='드라마') # genreNm
# director = Director()
# movie = Movie()

# if response.get('display') == 0:
#     pass
# elif response.get('display') == 1:
#     pass



# else:
#     for item in response['items']:
#         if item['director'].replace('|','') == directors:



            # break
