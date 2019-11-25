from django.shortcuts import render,get_object_or_404
from bs4 import BeautifulSoup
from urllib.request import urlopen
from decouple import config
from datetime import datetime, timedelta
from pprint import pprint
from .models import Actor, Director, Movie, Rating, Genre
import requests
from IPython import embed

# Create your views here.
def index(request):
    return render(request, 'movies/index.html')


def getmovies(request):
    cover = {}
    for i in range(10):
        targetDt = datetime(2018, 11, 20) - timedelta(weeks = i )
        targetDt = targetDt.strftime(f'%Y%m%d') # strftime : str특정 포멧으로 바꾸게 해준다.

        key = config('API_KEY')
        weekGb = 0 # 주일 + 주말
        base_url ='http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json' 
        api_url = f'{base_url}?key={key}&targetDt={targetDt}&weekGb={weekGb}'
        response = requests.get(api_url)
        data = response.json()
        for rank in range(len(data['boxOfficeResult']['weeklyBoxOfficeList'])):
                if data['boxOfficeResult']['weeklyBoxOfficeList'][rank]['movieCd'] in cover.keys():
                # if data['boxOfficeResult']['weeklyBoxOfficeList'][rank]['movieCd'] in cover[data['boxOfficeResult']['weeklyBoxOfficeList'][rank]['movieCd']].keys(): # 코드 번호
                    pass
                else:
                    cover.update({
                    data['boxOfficeResult']['weeklyBoxOfficeList'][rank]['movieCd'] :
                        {
                        'movieNm' : data['boxOfficeResult']['weeklyBoxOfficeList'][rank]['movieNm'],
                        }
                    })
    
    base_url ='http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json'
    key = config('API_KEY')
    movie_info = []
    for k, v in cover.items():
        api_url = f'{base_url}?key={key}&movieCd={k}'
        response = requests.get(api_url)
        data = response.json()
        movieCd = k
        movieNm = data['movieInfoResult']['movieInfo']['movieNm']
        actors_yjw = data['movieInfoResult']['movieInfo']['actors']
        director_yjw = data['movieInfoResult']['movieInfo']['directors'][0]
        genres = data['movieInfoResult']['movieInfo']['genres']
        pprint(data)
        
        BASE_URL = 'https://openapi.naver.com/v1/search/movie.json'
        
        ID = config('CLIENT_ID')
        SECRET = config('CLIENT_SECRET')

        HEADERS = {
            'X-Naver-Client-id' : ID,
            'X-Naver-Client-Secret' : SECRET,
        }
        # naver
        query = data['movieInfoResult']['movieInfo']['movieNm']
        API_URL = f'{BASE_URL}?query={query}'
        response = requests.get(API_URL, headers=HEADERS).json()  # naver
        if response['display'] == 1:
            poster_url = response['items'][0]['image']
            link = response['items'][0]['link']
            actors_naver =  list(filter(lambda x: x != "", response['items'][0]['actor'].split('|')))

            #img
            html = urlopen(link)
            source = html.read()
            html.close()
            soup = BeautifulSoup(source,'html.parser')
            div = soup.find('div','people')
            iag_alt = div.find_all('img')
            for d in iag_alt:
                if d.attrs['alt'] == director_yjw:
                    print(d.attrs['alt'])  # 영화배우 혹은 감독 이름
                    print(d.attrs['src'])  # 이미지

                
                if d.attrs['alt'] in actors_yjw:
                    
                    print(d.attrs['alt'])  # 영화배우 혹은 감독 이름p
                    print(d.attrs['src'])  # 이미지



        elif response['display'] >1:
            for item in response['items']:
                directors =  list(filter(lambda x: x != "", response['items'][0]['director'].split('|')))
                if director_yjw in directors:
                    
                    break
        else:
            pass               




        # pprint(response)
        # genre_id =  get_object_or_404(Genre, genreNm=genreNm).id

        # if response.get('display') == 0:
        #     pass
        # elif response.get('display') == 1:
            
            


    context = {
        'api_url' : api_url,
    }
    return render(request, 'movies/index.html', context)
