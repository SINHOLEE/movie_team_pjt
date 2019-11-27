from django.shortcuts import render,get_object_or_404,redirect
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from bs4 import BeautifulSoup
from urllib.request import urlopen
from decouple import config
from datetime import datetime, timedelta
from pprint import pprint
from .models import Actor, Director, Movie, Rating, Genre
from accounts.models import User
from .forms import RatingForm
from django.contrib.auth import get_user_model
import requests
from IPython import embed


# Create your views here.
def index(request):
    movies = Movie.objects.all()
    user = request.user
    if user.is_authenticated:
        genres = user.liked_genres.all()
        bucket = [[],[],[]]
        if len(genres) == 3:
            for i in range(3):
                genre = genres[i]
                cnt = 0
                bucket[i].append(genre)
                for movie in movies:
                    if genre in movie.genre.all():
                        bucket[i].append(movie)
                        cnt += 1
                    if cnt == 6:
                        break
        pprint(bucket)
    else:
        bucket = []   
        genres = [1]
    context = {
   
        'bucket' : bucket,
        'movies' : movies,
        'genres':genres,
        'genres_length' : len(genres),
        }
    return render(request, 'movies/index.html', context)

# detail에서는 로그인 해야 form이 보여져야 한다.
@require_GET
def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    genres = movie.genre.all()
    actors = movie.actor.all()
    director = movie.director.get()
    form = RatingForm()
    ratings = movie.ratings.all()
    context = {
        'movie':movie,
        'genres':genres,
        'actors':actors,
        'director':director,
        'form': form,
        'ratings':ratings,
    }
    return render(request, 'movies/detail.html', context)


@login_required
def like(request, movie_pk):
    user = request.user
    movie = get_object_or_404(Movie, pk=movie_pk)

    if user in movie.liked_users.all():
        user.liked_movies.remove(movie)
        liked = False
    else:
        user.liked_movies.add(movie) 
        liked = True

    context = {
        'liked':liked,
        'count': movie.liked_users.count()
    }

    return JsonResponse(context)
    
@require_POST
def rating(request, movie_pk):
    if request.user.is_authenticated:
        form = RatingForm(request.POST)
    
        if form.is_valid():
            rating = form.save(commit=False)
            rating.movie_id = movie_pk
            rating.user = request.user
            rating.save()


        return redirect('movies:detail', movie_pk)


@login_required
def update_rating(request, rating_pk):
    rating = get_object_or_404(Rating, pk=rating_pk)
    movie_pk = rating.movie_id
    movie = get_object_or_404(Movie, pk=movie_pk)
    ratings = movie.ratings.all()
    if request.method == 'POST':
        form = RatingForm(request.POST, instance=rating)
        if form.is_valid():
            form.save()
            form = RatingForm()
            context = {
                'movie': movie,
                'ratings': ratings,
                'form': form,        
            }
    else: 
        form = RatingForm()
        updateform = RatingForm(instance=rating)
        context = {
            'movie': movie,
            'ratings': ratings,
            'form': form,   
            'updateform': updateform, 
            'rating_pk': rating_pk, 
        }
    return render(request, 'movies/detail.html', context)


@require_POST
def delete_rating(request, rating_pk):
    rating = get_object_or_404(Rating, pk=rating_pk)
    movie_pk = rating.movie_id
    if rating.user == request.user:
        rating.delete()
    return redirect('movies:detail', movie_pk)


def getmovies(request):
    cover = {}
    embed()
    return
    for i in range(10):
        targetDt = datetime(2019, 11, 21) - timedelta(weeks = i )
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
        if Movie.objects.filter(code=k):
            continue

        try:
            movieCd = k
            movieNm = data['movieInfoResult']['movieInfo']['movieNm']
            actors_yjw = list(map(lambda x: x['peopleNm']  ,data['movieInfoResult']['movieInfo']['actors']))
            director_yjw = data['movieInfoResult']['movieInfo']['directors'][0]['peopleNm']
            genres = list(map(lambda x: x['genreNm']  , data['movieInfoResult']['movieInfo']['genres']))
            
        
            for genre1 in genres:
                if Genre.objects.filter(genreNm=genre1):
                    continue
                genre = Genre()
                genre.genreNm = genre1
                genre.save()
            

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
            actor_lis = []
            if response['display'] == 1:

                poster_url1 = response['items'][0]['image']
                link = response['items'][0]['link']
                actors_naver =  list(filter(lambda x: x != "", response['items'][0]['actor'].split('|')))
                #img
                html = urlopen(link)
                source = html.read()
                html.close()
                soup = BeautifulSoup(source,'html.parser')
                description = soup.find('p','con_tx').get_text()
                div = soup.find('div','people')
                iag_alt = div.find_all('img')
                print('movie_code', k)  # 영화 코드
                ac_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json'
                key = config('API_KEY')
                for d in iag_alt:
                    if d.attrs['alt'] == director_yjw:
                        # print(d.attrs['alt'], '감독')  # 영화배우 혹은 감독 이름
                        # print(d.attrs['src'])  # 이미지
                        src = d.attrs['src']
                        directorNm = d.attrs['alt']
                        url = f'{ac_url}?key={key}&peopleNm={directorNm}'
                        response = requests.get(url)
                        data = response.json()
                        flag = False
                        if data['peopleListResult']['totCnt'] == 1:
                            director_cd =  data['peopleListResult']['peopleList'][0]['peopleCd']
                            flag = True
                        elif data['peopleListResult']['totCnt'] >1:
                            for i in range(data['peopleListResult']['totCnt']):
                                filmos = list(filter(lambda x: x != "", data['peopleListResult']['peopleList'][i]['filmoNames'].split('|'))) 
                                if movieNm in filmos:
                                    director_cd =  data['peopleListResult']['peopleList'][i]['peopleCd']
                                    flag = True
                                    break
                        if flag: 
                            if Director.objects.filter(director_cd=director_cd):
                                continue
                            director = Director()
                            director.director_cd = director_cd
                            director.directorNm =  director_yjw
                            director.img_url = src
                            director.save()                        
                    if d.attrs['alt'] in actors_yjw:
                        actorNm = d.attrs['alt']
                        # print(d.attrs['alt'], '배우')  # 영화배우 혹은 감독 이름p
                        # print(d.attrs['src'])  # 이미지
                        src = d.attrs['src']
                        url = f'{ac_url}?key={key}&peopleNm={actorNm}'
                        response = requests.get(url)
                        data = response.json()
                        flag = False
                        if data['peopleListResult']['totCnt'] == 1:
                            actor_cd =  data['peopleListResult']['peopleList'][0]['peopleCd']
                            flag = True
                        elif data['peopleListResult']['totCnt'] >1:
                            for i in range(data['peopleListResult']['totCnt']):
                                filmos = list(filter(lambda x: x != "", data['peopleListResult']['peopleList'][i]['filmoNames'].split('|'))) 
                                if movieNm in filmos:
                                    actor_cd =  data['peopleListResult']['peopleList'][i]['peopleCd']
                                    flag = True
                                    break
                        if flag: 
                            if Actor.objects.filter(actor_cd=actor_cd):
                                continue
                            actor_lis.append(actor_cd)
                            actor = Actor()
                            actor.actorNm = actorNm
                            actor.img_url = src
                            actor.actor_cd = actor_cd
                            actor.save()

                
            elif response['display'] >1:
                for item in response['items']:
                    directors =  list(filter(lambda x: x != "", response['items'][0]['director'].split('|')))
                    if director_yjw in directors:
                        poster_url1 = item['image']
                        link = item['link']
                        actors_naver =  list(filter(lambda x: x != "", item['actor'].split('|')))

                        #img
                        html = urlopen(link)
                        source = html.read()
                        html.close()
                        soup = BeautifulSoup(source,'html.parser')
                        description = soup.find('p','con_tx').get_text()

                        div = soup.find('div','people')
                        iag_alt = div.find_all('img')
                        print('movie_code', k)  # 영화 코드
                        ac_url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json'
                        key = config('API_KEY')
                        for d in iag_alt:
                            if d.attrs['alt'] == director_yjw:
                                # print(d.attrs['alt'], '감독')  # 영화배우 혹은 감독 이름
                                # print(d.attrs['src'])  # 이미지
                                src = d.attrs['src']
                                directorNm = d.attrs['alt']
                                url = f'{ac_url}?key={key}&peopleNm={directorNm}'
                                response = requests.get(url)
                                data = response.json()
                                flag = False
                                if data['peopleListResult']['totCnt'] == 1:
                                    director_cd =  data['peopleListResult']['peopleList'][0]['peopleCd']
                                    flag = True
                                elif data['peopleListResult']['totCnt'] >1:
                                    for i in range(data['peopleListResult']['totCnt']):
                                        filmos = list(filter(lambda x: x != "", data['peopleListResult']['peopleList'][i]['filmoNames'].split('|'))) 
                                        if movieNm in filmos:
                                            director_cd =  data['peopleListResult']['peopleList'][i]['peopleCd']
                                            flag = True
                                            break
                                if flag: 
                                    if Director.objects.filter(director_cd=director_cd):
                                        continue
                                    director = Director()
                                    director.director_cd = director_cd
                                    director.directorNm =  director_yjw
                                    director.img_url = src
                                    director.save()                        
                            if d.attrs['alt'] in actors_yjw:
                                actorNm = d.attrs['alt']
                                src = d.attrs['src']
                                # print(d.attrs['alt'], '배우')  # 영화배우 혹은 감독 이름p
                                # print(d.attrs['src'])  # 이미지
                                src = d.attrs['src']
                                url = f'{ac_url}?key={key}&peopleNm={actorNm}'
                                response = requests.get(url)
                                data = response.json()
                                flag = False
                                if data['peopleListResult']['totCnt'] == 1:
                                    actor_cd =  data['peopleListResult']['peopleList'][0]['peopleCd']
                                    flag = True
                                elif data['peopleListResult']['totCnt'] >1:
                                    for i in range(data['peopleListResult']['totCnt']):
                                        filmos = list(filter(lambda x: x != "", data['peopleListResult']['peopleList'][i]['filmoNames'].split('|'))) 
                                        if movieNm in filmos:
                                            actor_cd =  data['peopleListResult']['peopleList'][i]['peopleCd']
                                            flag = True
                                            break
                                if flag: 
                                    if Actor.objects.filter(actor_cd=actor_cd):
                                        continue
                                    actor_lis.append(actor_cd)

                                    actor = Actor()
                                    actor.actorNm = actorNm
                                    actor.img_url = src
                                    actor.actor_cd = actor_cd
                                    actor.save()
                        break   
            if Movie.objects.filter(poster_url=poster_url1):
                continue
            movie = Movie()
            movie.movieNm = movieNm
            movie.code = k
            movie.poster_url = poster_url1
            movie.link_url = link
            movie.description = description  
            
            movie.save()
            directors = Director.objects.filter(director_cd=director_cd)
            # embed()
            print('actor_list', actor_lis)
            for actorCd in actor_lis:
                print('actor_code', actorCd)
                actor = Actor.objects.filter(actor_cd=actorCd).first()
                print('actor', actor)
                actor.movies.add(movie)
            for director in directors:
                # print(director)
                movie.director.add(director)
            for genre in genres:
                genre = Genre.objects.get(genreNm=genre)
                movie.genre.add(genre)
            
        except:
            continue

    return redirect('movies:index') 
