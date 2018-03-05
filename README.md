# safercar

## TODO:

- [x] 검색부터 구현
- [x] index
- [x] 차량 상세 정보
- [x] 결함 목록
- [x] 검색 결과 목록
- [x] 썸네일
- [x] 비슷한 발음 검색 지원 (싼타페, 산타패)
- [ ] 자동완성
- [ ] 공유
- [ ] OGP 이미지
- [x] 이름 정하기(자동차 결함정보 포털 -> ??)
- [x] 도메인 정하기
- [ ] 푸터 (github 링크, 후원 링크)
- [ ] 상세정보 레이아웃 (탭, 진행중 하일라이트)
- [ ] 댓글
- [ ] VIN CODE 검색
- [ ] GA


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


## DATA:

- [v] 모델명, 세대명 분리. 세대명을 위한 별도 col 필요함
- [v] 뉴/New 정리 

## 개발서버 실행:
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


**참고**

- 4년마다 리비젼, 2년마다 페이스리프트 등의 생산 주기 고려
- 시트에서 결함 발견할 때마다 셀에 메모 남기기 (e.g., LF쏘나타, 쏘나타LF !?)
- 결함 순, 리콜 순 나열하기
- https://pypi.python.org/pypi/vinlib/ VIN 라이브러리
- https://www.nicb.org/how-we-help/vincheck VIN 조회
- https://www.autocheck.com/vehiclehistory/autocheck/en/ VIN 조회
- https://www.dmv.org/vehicle-history/vin-decoder.php
- https://www.npmjs.com/package/vehicle-identification-number

**자동차상식**

- BOM을 참고하여 부품 체계 파악
- 캠페인(이벤트같은 버그픽스) < 무상수리 < 리콜
