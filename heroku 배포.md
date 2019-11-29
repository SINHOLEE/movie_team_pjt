heroku 배포

```bash
#1 branch 생성
$git branch heroku
$git checkout heroku

#2 heroku install (환경을 설정해주는 라이브러리 설치만 하면 된다.)
$pip install django-heroku

#3 헤로쿠에 올렸을 때 어떤일을 하라는 명령을 내리는 곳
$vi Procfile
web: gunicorn movie_pjt.wsgi --log-file -
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
~
procfile[+] [unix] (08:59 01/01/1970)                                                                               
#4 gunicorn install
$pip install gunicorn

#5 다시 requirements.txt 만들기
$ pip freeze > requirements.txt

### pywin32 pypiwin32 파일 있으면 지워라

#6 runtime.txt 생성
python-3.7.4 # 현재 파이썬 버전정보 입력

#7 settings.py
from decouple import config
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG')

ALLOWED_HOSTS = ['*']



STATIC_URL = '/static/'
STATIC_ROOT =  os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

AUTH_USER_MODEL = 'accounts.User' # 앱이름.모델이름


import django_heroku
django_heroku.settings(locals())



#8 .env 생성 후 config에 넣는다.

#9 구글에 heroku 로그인 후 heroku.com으로 돌아온다.

#10 검색창에 heroku cli 검색
#11 Dev Center 클릭
#12 The Heroku CLI
#13  window 64bit install

#14 켜져있는 모든 vscode 다껐다키고 
#15 다음과 같은 커멘트를 입력했하면 정상적으로 작동한다.
$heroku
#16 
$ heroku login
#17 헤로쿠 프로젝트 생성
$ heroku create sh-jy-movie-pjt

#18 .env heroku setting
heroku dashboard > sh-jy-movie-pjt > settings > config Vars > 추가

#19 add / commit 한 뒤

$git remote add heroku https://git.heroku.com/final-sh-jy-movie-project.git
# 20 의미 git push한다 heroku라는 리모드에 헤로쿠라는 브런치의 작업내용을 헤로쿠 리모트의 마스터에 올리;겠다.
$ git push heroku heroku:master


```

