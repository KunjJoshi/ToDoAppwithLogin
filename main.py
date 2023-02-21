from fastapi import FastAPI,Request,Depends,status,Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
import models
from database import engine,sessionlocal
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles
import datetime
models.Base.metadata.create_all(bind=engine)
templates=Jinja2Templates(directory='templates')
SECRET='our-secret-key'
app=FastAPI()
manager=LoginManager(SECRET,token_url='/auth/login',use_cookie=True)
manager.cookie_name='some-name'
app.mount('/static',StaticFiles(directory='static'),name='static')
def getdb():
    db=sessionlocal()
    try:
        yield db
    finally:
        db.close()
DB={'Kunj':{'password':'kunjjoshi'},'Wobot':{'password':'wobotai'}}
@manager.user_loader()
def loaduser(username:str):
    user=DB.get(username)
    return user
@app.post('/auth/login')
def login(data:OAuth2PasswordRequestForm=Depends()):
    username=data.username
    password=data.password
    user=loaduser(username)
    if not user:
        raise InvalidCredentialsException
    elif password!=user['password']:
        raise InvalidCredentialsException
    access_token=manager.create_access_token(data={'sub':username})
    resp=RedirectResponse('/index',status_code=status.HTTP_302_FOUND)
    manager.set_cookie(resp,access_token)
    return resp
@app.get('/')
async def loginpage(request:Request):
    return templates.TemplateResponse('checklog.html',{'request':request})
@app.get('/index')
async def home(request:Request,db:Session=Depends(getdb)):
    todos=db.query(models.Todo)
    return templates.TemplateResponse('index.html',{'request':request,'todos':todos})
@app.post('/add')
async def add(request:Request,task:str=Form(...),time:str=Form(...),db:Session=Depends(getdb)):
    todo=models.Todo(task=task)
    todo.time=time
    db.add(todo)
    db.commit()
    return RedirectResponse(url=app.url_path_for('home'),status_code=status.HTTP_303_SEE_OTHER)
@app.get('/edit/{todo_id}')
async def add(request:Request,todo_id:int,db:Session=Depends(getdb)):
    todo=db.query(models.Todo).filter(models.Todo.id==todo_id).first()
    return templates.TemplateResponse('edit.html',{'request':request,'todo':todo})
@app.post('/edit/{todo_id}')
async def add(request:Request,todo_id:int,task:str=Form(...),time:str=Form(...),completed:bool=Form(False),db:Session=Depends(getdb)):
    todo=db.query(models.Todo).filter(models.Todo.id==todo_id).first()
    now=datetime.datetime.now()
    todo.time=time
    time=datetime.datetime.strptime(todo.time,'%H:%M')
    if now>time:
        todo.completed=True
    else:
        todo.completed=completed
    db.commit()
    return RedirectResponse(url=app.url_path_for('home'),status_code=status.HTTP_303_SEE_OTHER)
@app.get('/delete/{todo_id}')
async def add(request:Request,todo_id:int,db:Session=Depends(getdb)):
    todo=db.query(models.Todo).filter(models.Todo.id==todo_id).first()
    db.delete(todo)
    db.commit()
    return RedirectResponse(url=app.url_path_for('home'),status_code=status.HTTP_303_SEE_OTHER)
