# gwanghwamun_suggestion
## 개요
* 청와대 국민청원 :  문재인 정부 출범 이후 청와대 웹사이트에서 국민이 청원을 제시하여 SNS 계정으로 로그인한 20만 명의 추천을 받으면 책임자가 답변을 하는 제도이다. 이 제도에서 등장하고 토론한 안건을 살펴본다.

## 순서
1. 데이터 수집(크롤링 및 저장)
2. 데이터 분석
    * 통계
    * word cloud
    * word to vec (k-mean cluster)

### requirements
* pip install -r requirements.txt 
* KoNLPy - 설치참고(https://konlpy.org/ko/latest/install/)

### path
* Crawling
    1. driver_path : __Users\chromedriver.exe__
    2. data_save_path : __Users\data__

    
* Analysis_path
    1. root : __Users\data__ (folder)


* word_cloud_path : 
    1. root : __Users\data__ (folder)
    2. img_path : __Users\setting\img__ (jpg,png ..)
    3. font_path : __Users\setting\font__ (tiff)


* word2vec_path :
    1. root : __Users\data__ (folder)
    2. font_path : __Users\setting\font__ (tiff)

## 데이터출처
* 광화문1번가(https://www.gwanghwamoon1st.go.kr/front/main/index.do)
* 정책제안 -> 혁신제안톡 -> 전체

## Report
### data
1. 데이터는 crawling 된 데이터를 사용함.
2. crawling 시각은 2020-05-24,18-09 을 기준으로 분석,시각화를 진행함.

### analysis
* 구분별 청원횟수
    1. 데이터의 구분목록(보건의료,공공행정,교육,기타 등...)을 추출하여 각 값을 count 후 그래프 생성
    2. ![이미지](src/img/구분별청원횟수.png)
    3. 확인결과 기타가 542로 가장 높으며, 다음으로 보건의료,공공행정,사회복지 등이 등장,가장 낮은 부분은 통일외교로 8건 밖에 해당하지 않음 


* 진행상황별 목록
    1. 데이터의 진행상황(토론종료,토론중,숙성중,과제추친중,숙성종료)을 추출하여 각 값을 count 후 그래프 생성
    2. ![이미지](src/img/진행상황별목록횟수.png)

* 생성날짜별 청원횟수
    1. 데이터의 생성날짜를 추출하여 각 값을 count 후 그래프 생성
    2. ![이미지](src/img/생성날짜별청원횟수.png)
    
    3. 청원횟수가 20회 이상인 날은 다음과 같다. 20회인 이상의경우 날짜별 word cloud 를 생성함. 
    4. 
        |생성날짜목록 | 청원횟수|
        |:----:|----:|
        | 2020-04-01 |   120|
        | 2018-10-30 |   103|
        | 2019-03-04 |   100|
        | 2019-04-30 |    69|
        | 2019-03-05 |    56|
        | 2020-03-31 |    54|
        | 2019-11-21 |    49|
        | 2019-03-30 |    48|
        | 2019-10-10 |    45|
        | 2020-04-04 |    45|
        | 2019-10-11 |    28|
        | 2019-11-07 |    25|
        | 2019-11-20 |    24|

 * 구분별 좋아요수
    1. 데이터의 구분별 좋아요수를 추출하여 각 값을 count 후 그래프 생성
    2. ![이미지](src/img/구분별좋아요수.png)
    3. 각 구분별 좋아요수의 mean 과 max는 아래와 같다.
    4. 
        | 구분 | Mean | Max |
        |:----:|----:|----:|
        |공공행정|1.571|   40|
        |과학기술|1.000|   10|
        |교육|5.186|   51|
        |교통물류|2.156|   47|
        |국토관리|0.762|    4|
        |기타|3.120|  164|
        |농축수산|0.643|    5|
        |문화관광|11.529|   83|
        |보건의료|4.460|  163|
        |사회복지|6.618|  269|
        |산업고용|2.146|   42|
        |식품건강|2.750|   33|
        |재난안전|1.892|   40|
        |재정금융|2.031|   33|
        |통일외교|0.625|    1|
        |환경기상|0.878|    5|
    5. 각 구분별 word_cloud 를 생성함.

### word_cloud
#### all_word_cloud 
* ![이미지](src/img/all_word_cloud.png)

* all_word_cloud 에서 보이는 주요 단어는 어르신,부모님,제안,생각,운전,사회,음주,공무원,마음 등이 먼저 눈에 들어온다.

### date_word_cloud
* ![이미지](src/img/date_word_cloud/2018-10-30_word_cloud.png)

* 제안하는 사이트가 정부혁신1번가 -> 광화문1번가로 바뀌면서 이전에 기록된 데이터들이 모두 2018-10-30 으로 이동한것으로 보인다.
* 주요 키워드는 : 이유,국민,시설,청년,정부,교육 등이 보인다.

특히나 이후 청원횟수가 20회 이상인 날의 word_cloud 의 경우 다른특이점을 보이지 않으나 2020-03-31의 word_cloud에서부터 코로나,마스크가 등장하기 시작한다.
* ![이미지](src/img/date_word_cloud/2020-03-31_word_cloud.png)

2020-04-01 은 마스크,약국,취약,계층,구매,시간,배달 등의 단어로 미루어보아 코로나의 여파임 알수있다.

* ![이미지](src/img/date_word_cloud/2020-04-01_word_cloud.png)

### division_word_cloud
* ![이미지](src/img/division_word_cloud/%EA%B8%B0%ED%83%80_word_cloud.png)

* 가장 많은 구분항목인 __기타__ 에서 등장한 단어들은 위와 같다.
* 눈에띄는 단어들은 국민,사회,이유,학생,미국,개선,정부,사람,주택 등 전반적인 사회정치 단어가 보인다.

### word2vec

#### title
* ![이미지](src/img/word2vec_title.png)
* window_int=3,min_cnt=19,num_cluster=5
* 대체적으로 의미있는 단어끼리 군집화가 잘 이루어진것으로보인다.

#### text
* ![이미지](src/img/word2vec_text.png)
* window_int=5,min_cnt=230,num_cluster=6
* 단어의 의미는 서로 군집화가 잘이루어졌으나, title 에 비해 많은양의 단어로 인해 만은차원의 생성, 그리고 차원축소의 과정에서 한눈에 알아보기 힘든 img 이다.