from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles

class Memo(BaseModel):
    id:int
    content:str

memos = []

app = FastAPI()

@app.post('/memos')
def create_memo(memo:Memo):
    memos.append(memo) 
    return "메모 추가에 성공했습니다."

@app.get('/memos')
def read_memo():
    return memos

@app.put("/memos/{memo_id}")
def put_memo(req_memo:Memo):
    for memo in memos: 
        if memo.id == req_memo.id:
            memo.content = req_memo.content
            return '성공했습니다.'
    return '그런 메모는 없습니다'            

@app.delete("/memos/{memo_id}")    
def delete_memo(memo_id):
    for index, memo in enumerate(memos): 
        if str(memo.id) == str(memo_id):
            memos.pop(index)
            return('삭제성공')

    return('삭제실패')

app.mount("/", StaticFiles(directory="static", html=True), name="static")







