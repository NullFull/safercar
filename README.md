# safercar

## 논의
슬랙 https://nullfull.slack.com 안 #kh-power 채널에서 개발 논의가 진행중입니다.

https://nullfull-slack-invite.herokuapp.com/ 에서 셀프 초대가 가능합니다.

## log

DONE:

- 검색부터 구현
- index
- 차량 상세 정보
- 결함 목록
- 검색 결과 목록
- 썸네일
- 비슷한 발음 검색 지원 (싼타페, 산타패)
- 자동완성
- 이름 정하기(자동차 결함정보 포털 -> ??)
- 도메인 정하기
- 공유 #슬님
- OGP 이미지 #혜정님 #슬님
- 푸터 (github 링크, 뉴스타파 후원 링크) #혜정님
- 댓글 #슬님
- GA #슬님
- 탭 네비게이션을 만든다 (리콜 | 무상수리 | 비공인 무상수리 | 급발진 의심신고 | 댓글) #원님
  - 탭을 누르면 해당 카테고리 결함을 볼 수 있다
  - 개수가 0인 카테고리 탭은 비활성화 하지만 정보로서 위계는 유지하는 선에서 정리
- 데이터 임포터에 변경된 필드를 반영한다 #슬님
- 비공인 무상수리 모델용 레이아웃을 만든다 #슬님
  - 비공인 무상수리 탭에 동호회 리스트를 표시한다
  - 동호회의 활/비활성화 상태를 표시한다
- 도메인(checkyourcar.net) #슬님
  - 연결하기
  - 구입하기
- 자동완성 기능추가
  - 키보드 네비게이션
  - 최대표시 개수 설정
- 제조사 검색기능
  - 다양한 상세 모델명들을 검색 키워드로 활용할 수 있도록 만들기(특히 5시리즈)

TODO:

- [ ] 검색창 자동완성 리팩토링
- [ ] 결함 리스트 리팩토링
  - 현재 진행중인 조치사항은 강조표시한다 (카드 우측상단 활용)
- [ ] VIN CODE 검색

일정:

- ~~베타: 2/28~~
- ~~오픈: 3/19~~


## 이름 후보:

- H.K. Power(Heum Kyul power)
- 결함타파
- 내차다이죠부deathcar?
- 내차언-제다이
- 결함차요
- 내차속의결함
- 수리수리무상수리
- 한없이 리콜에 가까운 내차
- 어디까지 받아봤니 무상수리
- 수리받자
- 소원수리
- 또탈리콜(ddotalrecall.?)
- 이래도 탈래
- 안돼 현기야
- 현기차 (고장)난단말이에요...
- 내차 이따이
- 외않리콜?
- 리콜가즈아!
- 마이결함카
- 내차의과거
- (무상수리)어디까지 알아보고 오셨어요?
- **자동차 결함정보 포털**

## DATA

- [x] 모델명, 세대명 분리. 세대명을 위한 별도 col 필요함
- [x] 뉴/New 정리

## 개발서버 실행

### 데이터 불러오기

데이터는 구글 스프레드시트 내용을 불러오고 있음.
접근 권한은 settings에 GSPREAD_AUTH에 Google Service Account 내용을 넣고 (원하는 분은 @lexifdev 에게 연락) django 명령으로 불러옴.

```python
# settings.py
GSPREAD_AUTH = {
  "type": "service_account",
  "private_key": "...",
  "client_email": "...",
  ...
}
```

```
$ python manage.py import_data
```

### 썸네일 생성

data/cars에 있는 사진들을 기반으로 static 안에 썸네일들을 생성함

```
$ python manage.py convert_images
```

### 서버 실행

```
$ python manage.py runserver
```

## 배포

메인 실서버 반영은 @lexifdev 에게 연락


참고:

- 4년마다 리비젼, 2년마다 페이스리프트 등의 생산 주기 고려
- 시트에서 결함 발견할 때마다 셀에 메모 남기기 (e.g., LF쏘나타, 쏘나타LF !?)
- 결함 순, 리콜 순 나열하기
- https://pypi.python.org/pypi/vinlib/ VIN 라이브러리
- https://www.nicb.org/how-we-help/vincheck VIN 조회
- https://www.autocheck.com/vehiclehistory/autocheck/en/ VIN 조회
- https://www.dmv.org/vehicle-history/vin-decoder.php
- https://www.npmjs.com/package/vehicle-identification-number

자동차상식:

- BOM을 참고하여 부품 체계 파악
- 캠페인(이벤트같은 버그픽스) < 무상수리 < 리콜
