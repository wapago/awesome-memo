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

def get_memo_from_mongodb():
    memos_in_db = list(collection.find({}, {"_id": 0})) # mongodb atlas에 저장된 객체고유id는 제외하고 반환
    return memos_in_db

app = FastAPI()

@app.post('/memos')
def create_memo(memo:Memo):
    data_to_insert = dict(memo)
    collection.insert_one(data_to_insert)

    return "메모 추가에 성공했습니다."


@app.get('/memos')
def read_memo(order : Optional[str] = None, createAt: Optional[str] = None):
    memos_in_db = get_memo_from_mongodb()
    return memos_in_db

@app.put("/memos/{memo_id}")
def put_memo(req_memo:Memo):
    memos_in_db =get_memo_from_mongodb()
    for memo in memos_in_db:
        if memo['id'] == req_memo.id:
            collection.update_one(
                memo,
                {"$set": {"content": req_memo.content}}
            )
            return '성공했습니다.'
        
    read_memo()   

    return '그런 메모는 없습니다'            


@app.delete("/memos/{memo_id}")    
def delete_memo(memo_id):
    memos_in_db = get_memo_from_mongodb()
    for index, memo in enumerate(memos_in_db): 
        if str(memo.id) == str(memo_id):
            memos_in_db.pop(index)
            return('삭제성공')
        
    return('삭제실패')

app.mount("/", StaticFiles(directory="static", html=True), name="static")







