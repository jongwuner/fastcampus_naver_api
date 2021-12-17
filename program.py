import pandas
import requests
import json
import os

file_path = './'
# file_path = './drive/MyDrive/Fastcampus/Marketing/Part3/'


# EXCEL 저장 정보
column_name_list = [
  '제목',
  '링크',
  '이미지',
  '최저가',
  '최고가',
  '쇼핑몰',
  '상품유형',
  '브랜드',
  '제조사',
  '카테고리1',
  '카테고리2',
  '카테고리3',
  '카테고리4',
  ]


# NAVER API 고정 정보
X_NAVER_CLIENT_ID = '2y5X2WYXZiX10qbaSEUx'
X_NAVER_CLIENT_SECRET = 'T5ecs75fDD'


URL = 'https://openapi.naver.com/v1/search/shop.json' 
headers = {
  'X-Naver-Client-Id': X_NAVER_CLIENT_ID,
  'X-Naver-Client-Secret' : X_NAVER_CLIENT_SECRET 
}

print(headers['X-Naver-Client-Id'])
print(headers['X-Naver-Client-Secret'])


# NAVER API 호출 함수
def getItemListByNaver (query, display='5', sort='sim'):   
  params = {'query': query,'display':display,'sort':sort}
  res = requests.get(URL, headers=headers, params=params)
  resData = json.loads(res.text)['items']
  return resData

# NAVER ITEM 필터링 함수
def getFilteredItemList(itemList):
  def productTypeSpinner(productTypeNumber):
    if productTypeNumber == 1:
      return '일반 - 가격비교 상품'
    if productTypeNumber == 2:
      return '일반 - 가격비교 비매칭 일반상품'
    if productTypeNumber == 3:
      return '일반 - 가격비교 매칭 일반상품'
    if productTypeNumber == 4:
      return '중고 - 가격비교 상품'
    if productTypeNumber == 5:
      return '중고 - 가격비교 비매칭 일반상품'
    if productTypeNumber == 6:
      return '중고- 가격비교 매칭 일반상품'
    if productTypeNumber == 7:
      return '단종 - 가격비교 상품'
    if productTypeNumber == 8:
      return '단종 - 가격비교 비매칭 일반상품'
    if productTypeNumber == 9:
      return '단종 - 가격비교 매칭 일반상품'
    if productTypeNumber == 10:
      return '판매예정 - 가격비교 상품'
    if productTypeNumber == 11:
      return '판매예정 - 가격비교 비매칭 일반상품'
    if productTypeNumber == 12:
      return '판매예정 - 가격비교 매칭 일반상품'
    else:
      return '해당 없음'

  resItemList = []
  itemLen = len(itemList)
  for idx,item in enumerate(itemList):
    curFilteredItem = {
    'title' : item['title'],
    'link': item['link'],
    'image':item['image'],
    'lprice': item['lprice'],
    'hprice': item['hprice'],
    'mallName': item['mallName'],
    'productType': productTypeSpinner(int(item['productType'])),
    'brand': item['brand'],
    'maker': item['maker'],
    'category1': item['category1'],
    'category2': item['category2'],
    'category3': item['category3'],
    'category4': item['category4'],
    }
    resItemList.append(curFilteredItem.values())
    print(f">>> [{idx}/{itemLen}] 필터링 성공 ")

  return resItemList
    

# EXCEL 저장 함수
def saveInExcel(filteredItemList):
  df = pandas.DataFrame(filteredItemList, columns=column_name_list)
  df.to_excel(file_path+'output.xlsx', sheet_name='sample1')

query = '모니터'
# print(f">>> 입력한 검색어 : {query}")

# print('\n\nNAVER 정보를 불러오는 중 입니다...')
itemList = getItemListByNaver(query)
# print(f'>>> {len(itemList)}개 의 검색 결과를 불러왔습니다')
 
print('\n\nITEM 필터링을 시작합니다...')
filteredItemList = getFilteredItemList(itemList)
# print(f'>>> {len(filteredItemList)}개 의 필터링 된 데이터가 준비되었습니다')

print('\n\nExcel에 저장합니다...')
saveInExcel(filteredItemList)
