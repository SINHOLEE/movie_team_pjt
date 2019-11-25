from django.shortcuts import render,get_object_or_404
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
    for i in range(2):
        targetDt = datetime(2019, 11, 20) - timedelta(weeks = i )
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
    # pprint(cover)
    
    base_url ='http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json'
    key = config('API_KEY')
    movie_info = []
    for k, v in cover.items():
        api_url = f'{base_url}?key={key}&movieCd={k}'
        response = requests.get(api_url)
        data = response.json()
        
        if data['movieInfoResult']['movieInfo']['audits'] == []:
            pass
        else:
            watchGradeNm = data['movieInfoResult']['movieInfo']['audits'][0]['watchGradeNm']
        
        if data['movieInfoResult']['movieInfo']['genres'] == []:
            pass
        else:
            genreNm = data['movieInfoResult']['movieInfo']['genres'][0]['genreNm']
        
        if data['movieInfoResult']['movieInfo']['directors'] == []:
            pass
        else:
            directors = data['movieInfoResult']['movieInfo']['directors'][0]['peopleNm']
        
        temp = {
                'movieCd' : k,
                'movieNm' : data['movieInfoResult']['movieInfo']['movieNm'],
                'movieNmEn' : data['movieInfoResult']['movieInfo']['movieNmEn'],
                'movieNmOg' : data['movieInfoResult']['movieInfo']['movieNmOg'],
                'watchGradeNm' : watchGradeNm,
                'openDt': data['movieInfoResult']['movieInfo']['openDt'],
                'genreNm' : genreNm,
                'directors' : directors,
                }
        pprint(temp)
        
        BASE_URL = 'https://openapi.naver.com/v1/search/movie.json'
        
        ID = config('CLIENT_ID')
        SECRET = config('CLIENT_SECRET')

        HEADERS = {
            'X-Naver-Client-id' : ID,
            'X-Naver-Client-Secret' : SECRET,
        }

        query = data['movieInfoResult']['movieInfo']['movieNm']
        API_URL = f'{BASE_URL}?query={query}'
        response = requests.get(API_URL, headers=HEADERS).json()
        pprint(response)
        embed()
        genre_id =  get_object_or_404(Genre, genreNm=genreNm).id

        # if response.get('display') == 0:
        #     pass
        # elif response.get('display') == 1:
            
            


    context = {
        'api_url' : api_url,
    }
    return render(request, 'movies/index.html', context)
