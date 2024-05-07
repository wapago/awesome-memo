from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from typing import Optional
import pymongo

db_connection_str = "mongodb+srv://theanswerkk:rlacksgh3#@mongodb-learning.i9t8oz5.mongodb.net/?retryWrites=true&w=majority&appName=mongodb-learning"
client = pymongo.MongoClient(db_connection_str)
database = client.get_database("memos")
collection = database.get_collection("mongodb-learning")

class Memo(BaseModel):
    id:int
    content:str

memos = []

app = FastAPI()

@app.post('/memos')
def create_memo(memo:Memo):
    print(memo)
    
    data_to_insert = dict(memo)
    insert_result = collection.insert_one(data_to_insert)

    # 삽입 결과 확인
    print("====== Inserted document ID ======")
    print(insert_result.inserted_id)
    memos.append(memo) 
    return "메모 추가에 성공했습니다."


@app.get('/memos')
def read_memo(order : Optional[str] = None, createAt: Optional[str] = None):
    
    if(order == 'asc') :
        sorted_memos = sorted(memos, key=lambda x: x.content)

        if(createAt == 'asc'):
            sorted_memos = sorted(sorted_memos, key=lambda x: x.id)
        elif(createAt == 'desc'):
            sorted_memos = sorted(sorted_memos, key=lambda x: x.id, reverse=True)

        return sorted_memos
    elif(order == 'desc') :
        sorted_memos = sorted(memos, key=lambda x: x.content, reverse=True)

        if(createAt == 'asc'):
            sorted_memos = sorted(sorted_memos, key=lambda x: x.id)
        elif(createAt == 'desc'):
            sorted_memos = sorted(sorted_memos, key=lambda x: x.id, reverse=True)
            
        return sorted_memos
        
    return memos

@app.put("/memos/{memo_id}")
def put_memo(req_memo:Memo):
    print(req_memo.id)
    for memo in memos: 
        print(memo.id)
        if memo.id == req_memo.id:
            memo.content = req_memo.content
            return '성공했습니다.'
    return '그런 메모는 없습니다'            

# 2. "return('삭제실패')"가 for반복문 밖에 위치하는 경우
@app.delete("/memos/{memo_id}")    
def delete_memo(memo_id):
    # memos = [] 안의 memo를 하나씩 비교할 때
    for index, memo in enumerate(memos): 
        if str(memo.id) == str(memo_id):
            memos.pop(index)
            return('삭제성공')
    # for문 밖에 있으므로 모든 memos를 비교한 후에 같은 것이 없을 때 '삭제실패'를 return함
    return('삭제실패')

app.mount("/", StaticFiles(directory="static", html=True), name="static")







