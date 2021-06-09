# github issue crawler
- 깃헙의 이슈를 레파지토리 별로 크롤링 하는 프로젝트

# 설치
## 필수 요소 설치

1. install python3.8 [링크](https://www.python.org/downloads/)
   
   ```commandline
   python3.8 --version
   ```

2. upgrade pip

   ```commandline
   $ python3.8 -m pip --version
   $ python3.8 -m pip install --upgrade pip
   ```

3. install virtualenv
   
   ```commandline
   $ python3.8 -m pip install virtualenv virtualenvwrapper
   ```

4. 가상환경 설정

    - repository folder 안에서 하는 것으로 작성됐습니다.
   
   ```commandline
   $ pwd
   .../github-crawler/
   $ python3.8 -m virtualenv --python=python3.8 .env
   ```

## 환경 변수

1. Generate github personal access token

    - [참고자료](https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token)
    - 토큰에 부여해야하는 권한
        - workflow
        - repo
        - workflow 를 부여하면 repo 가 함께 부여됩니다.
        - issue 목록을 읽을 때, 다른 권한은 필요하지 않습니다.
    
2. 환경 변수 입력

   ```commandline
   $ vim .env/bin/activate
   ```
   ```
   export USER = <사용자 본인의 계정>
   export TOKEN = <사용자가 생성한 personal access token>
   export OWNER = <접근하고자 하는 repo의 owner 이름>
   ```

## 가상환경 실행

```commandline
$ . .env/bin/activate
(.env)$ 
```

## 의존성 모듈 설치

```commandline
(.env)$ pip install -r requirements.txt
```

# 실행

## 프로그래밍 실행

```commandline
(.env)$ python run.py
```

## 입력

1. csv 파일이 생성될 절대 경로를 입력
   
   - ex) `/Users/hyunwoo/Desktop/export`

2. 이슈 목록을 조회할 레파지토리를 목록의 숫자로 선택
