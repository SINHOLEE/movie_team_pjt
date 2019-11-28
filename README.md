# README







## Pair Programming

```
* Master : 이신호 / Slave : 신지영
* 마스터가 모델 작성 및 추천 알고리즘 등 핵심기능 구현
```



## 사용자 접근 경로

1. 신규회원 : 회원가입 -> 로그인 -> 선호 장르 3개 선택 -> 맞춤형 영화 추천 페이지로 이동 -> 장르별 검색 가능
2. 기존 회원 : 로그인 -> 맞춤형 영화 추천 페이지가 메인 페이지 -> 장르별 검색가능
3. 로그인 시, 영화 평점, 한줄평 남길 수 있음. 단, 1회 작성 시 추가 작성은 불가



## 추천 알고리즘 구현



### 로그인 한 유저가 3개 장르 선택 시 new_set에 저장

* views.py

```python

@require_POST
def get_like_genres(request):
    print(request.user)
    print(request.POST)
    user = request.user
    genres = ['genre1', 'genre2', 'genre3']
    flag = True
    new_set = set()
    for gn in genres:
        if request.POST.get(gn) not in new_set and request.POST.get(gn) != '':
            print('gn', gn)
            print('new_set', new_set)
            new_set.add(request.POST.get(gn))
        else:
            flag = False
            break
    if flag:
        for genre_item in genres:
            genre = Genre.objects.filter(genreNm=request.POST.get(genre_item).strip()).first()
            user.liked_genres.add(genre)

    else:
        pass 
    return redirect('movies:index')
        
```

```python
ebbunnim3
<QueryDict: {'csrfmiddlewaretoken': ['DRdap0q6PY2IvWv76dHcXpFPRvj5B01SsAI51lPvlknRBJY6mUc0jsYPWZzGcsO9'], 'genre1': ['애니메이션 '], 'genre2': ['어드벤처 '], 'genre3': ['멜로/로맨스 ']}>
gn genre1
new_set set()
gn genre2
new_set {'애니메이션 '}
gn genre3
new_set {'어드벤처 ', '애니메이션 '}
```



### index 페이지를 맞춤형 영화로 제시

* views.py

```python
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


def index(request):
    movies = Movie.objects.all()
    genres_all = Genre.objects.all()
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
        'priorities': [1,2,3],
        'genres_all':genres_all,
        'bucket' : bucket,
        'movies' : movies,
        'genres':genres,
        'genres_length' : len(genres),
        }
    return render(request, 'movies/index.html', context)



```

```python
< bucket 프린트 시> : 유저가 선택한 장르에 해당하는 영화 6개 추천 
[[<Genre: 애니메이션>,
  <Movie: Movie object (1)>,
  <Movie: Movie object (7)>,
  <Movie: Movie object (17)>,
  <Movie: Movie object (23)>,
  <Movie: Movie object (24)>,
  <Movie: Movie object (25)>],
 [<Genre: 어드벤처>,
  <Movie: Movie object (5)>,
  <Movie: Movie object (12)>,
  <Movie: Movie object (23)>,
  <Movie: Movie object (24)>,
  <Movie: Movie object (25)>,
  <Movie: Movie object (49)>],
 [<Genre: 멜로/로맨스>,
  <Movie: Movie object (7)>,
  <Movie: Movie object (9)>,
  <Movie: Movie object (14)>,
  <Movie: Movie object (20)>,
  <Movie: Movie object (22)>,
  <Movie: Movie object (40)>]]
 
```

* index.html

```html
{% load static %}
<!DOCTYPE html>
<!--...-->


  <div class="container">
  {% comment %} superuser에 한해서 영화 등록, 수정, 삭제가 이루어져야 한다는 것 반영 {% endcomment %}
{% if request.user.is_superuser  %}
<a href="{% url 'movies:getmovies' %}">영화정보 받기(관리자 전용 버튼)</a> 
{% endif %}
{% comment %} 수정, 삭제까지는 어떻게 구현해야? {% endcomment %}
<div id="app">
{% if request.user.is_authenticated %}


  <!--추가적으로 장르 선택하면 해당 장르에 맞는 영화들 리스트를 보여줌-->
    <div id="app" style="margin:0 auto">
        <select v-model="selected" style="color:black">
            <option v-for="option in options" v-bind:value="option.value"> 
                [[ option.text ]]
            </option>
        </select>
        {% comment %} <span>Selected: [[ selected ]]</span> {% endcomment %}
        <a :href="`movieby_genre/${selected}`"> [장르 선택 완료!] </a>
        <hr>
    </div> 


    {% if genres_length == 3%}
        {% for buk in bucket %}
            {% for movie in buk %}
                {% if movie in movies %}
                    {{ pass }}
                {% else %}
                    <p>{{ movie }}</p>
                {% endif %}
            {% endfor %}
            <li class='row'>
               
                {% for movie in buk %}
                    {% if movie in movies %}
                        
                              <div class="card" style="width: 18rem;">
                                <img src="{{ movie.poster_url }}" class="card-img-top" alt="사진">
                                <div class="card-body">
                                  <h6 class="card-title text-center">{{movie.movieNm}}</h6>
                                  {% comment %} <p class="card-text">{{movie.description}}</p> {% endcomment %}
                                  <a class="preview" href="  {% url 'movies:detail' movie.pk %} "><i class="fa fa-eye"></i> View Detail..
                                  {% comment %} <a  href="#movie-{{movie.pk}}" rel="prettyPhoto" ><i class="fa fa-eye"></i> View
                                  </a> {% endcomment %}
                                  </a>
                                </div>
                            </div>
                    {% endif %}
                {% endfor %}
            </li>
        {% endfor %}
    
    {% else %}

        <P>선호하는 장르를 선택해 주세요 꼭! 3가지 종류를 선택하시고, 중복선택을 지양해 주세요</P>

        <form action="{% url 'movies:get_like_genres' %}" method="POST" >
        {% csrf_token %}
        <div class="row form-group mb-1">
            {% for i in priorities %}
            <div class='card col-4 '>
                <label for="exampleFormControlSelect1">{{ i }}번째 선호 장르</label>
                <select class="form-control" name="genre{{i}}" id="exampleFormControlSelect1">
                    <option value="">선택</option>
                    {% for genreA in genres_all %}
                        <option value="{{ genreA }} ">{{ genreA }}</option>
                    {% endfor %}
                </select>
            </div>
            {% endfor %}
        </div>
        <button type="submit" class="btn btn-primary">등록</button>
        </form>
    {% endif %}
    
{% endif %}


<script>
    new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    data: {
        selected: '16',
        options: [
        { text: '애니메이션', value: '1' },
        { text: '범죄', value: '2' },
        { text: '드라마', value: '3' },
        { text: '액션', value: '4' },
        { text: '어드벤처', value: '5' },
        { text: 'SF', value: '6' },
        { text: '스릴러', value: '7' },
        { text: '판타지', value: '8' },
        { text: '멜로/로맨스', value: '9' },
        { text: '코미디', value: '10' },
        { text: '공포(호러)', value: '11' },
        { text: '가족', value: '12' },
        { text: '전쟁', value: '13' },
        { text: '미스터리', value: '14' },
        { text: '사극', value: '15' },
        { text: '기타', value: '16' },
        { text: '다큐멘터리', value: '17' },
        { text: '뮤지컬', value: '18' },
        ],
    }
    })
</script>

  </div>


<!--...-->

</body>
</html>

```



### 추가적으로 장르 검색 시 해당하는 영화목록 보여주기

* views.py

```python
# ..
def movieby_genre(request, genre_pk):
    genre = Genre.objects.get(pk=genre_pk)
    print(genre.movies.all())
    movies = genre.movies.all()
    print(movies)
    context = {
        'genre':genre,
        'movies':movies,
    }
    return render(request, 'movies/movieby_genre.html', context)
```



* Movie by_genre.html

```html

<!--...-->

    <h1 style="color:black">{{genre}}를(을) 검색하셨네요!</h1>
    <div class="row">
    {% for movie in movies  %}
        
        <div class="card" style="width: 18rem;">
                            <img src="{{ movie.poster_url }}" class="card-img-top" alt="사진">
                            <div class="card-body">
                                <h6 class="card-title text-center">{{movie.movieNm}}</h6>
                                {% comment %} <p class="card-text">{{movie.description}}</p> {% endcomment %}
                                <a class="preview" href="  {% url 'movies:detail' movie.pk %} "><i class="fa fa-eye"></i> View Detail..
                                {% comment %} <a  href="#movie-{{movie.pk}}" rel="prettyPhoto" ><i class="fa fa-eye"></i> View
                                </a> {% endcomment %}
                                </a>
                            </div>
                        </div>


    {% endfor %}
```

