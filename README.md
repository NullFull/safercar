# safercar

## 논의

슬랙 https://nullfull.slack.com 안 #kh-power 채널에서 개발 논의가 진행중입니다.

https://nullfull-slack-invite.herokuapp.com/ 에서 셀프 초대가 가능합니다.

## log

TODO:

- [ ] 검색창 자동완성 리팩토링
- [ ] 결함 리스트 리팩토링
  - 현재 진행중인 조치사항은 강조표시한다 (카드 우측상단 활용)
- [ ] VIN CODE 검색

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

## 기여하기

### 차량 이미지 수정

`data/cars/` 경로에 위치한 차량 이미지에서 배경을 없애주세요.

[전용 웹 서비스](https://www.remove.bg) 또는 포토샵 같은 프로그램을 사용하셔서, 아래 나쁜 예와 같은 이미지를 좋은 예와 같은 이미지로 교체해주세요.

나쁜 예:
![image](https://storage.googleapis.com/newstapa-apps.appspot.com/desucar/static/cars/a403-600x.png)

좋은 예:
![image](https://storage.googleapis.com/newstapa-apps.appspot.com/desucar/static/cars/hk01-600x.png)

주의사항:

- 새로운 이미지로 교체하시는 경우 이미지 라이선스를 지켜주세요.
- 이미지의 파일명을 유지해주세요.

---

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
