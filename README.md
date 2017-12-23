# safercar

## TODO:

- [ ] index 페이지 만들기(차량 조회)
- [ ] 대표 차종 한가지로 상세페이지 구성(산타페)
- [ ] 이름 정하기(자동차 결함정보 포털 -> ??)

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
  
- [ ] 소비자/소유주 별 메뉴 제공?
- [ ] 무상 수리 대상 부품을 사용하는 타 제조사의 차종 알아보기
- [ ] 작업중인 데이터 피드백
- [ ] 차량 조회 방법 정하기(생산일을 알 수 있는 가장 손쉬운 방법) VID?

## DATA:

- [ ] 모델명, 세대명 분리. 세대명을 위한 별도 col 필요함
- [ ] 세대명이 없다면 일단 비워두되, 모델명과 생산년도를 통해 도출

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
