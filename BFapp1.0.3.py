#to kill the proc: from portal write :ps
#kill bfapp
from datetime import datetime
import yagmail
from fastapi import FastAPI, HTTPException, Response, status
import pyodbc
import json
import notifiers
from fastapi_utils.tasks import repeat_every
from twilio.rest import Client

from starlette.requests import Request
import nest_asyncio
import uvicorn.logging
import uvicorn.loops.auto
import uvicorn.protocols.http.auto
import uvicorn.protocols.websockets.auto
import uvicorn.main
import uvicorn.lifespan.on
import uvicorn
import loguru
import time

# from Desktop.python.client import notifier

app = FastAPI()
# linux driver = ODBC Driver 17 for SQL Server
# win driver ={SQL SERVER}
try:
    db = pyodbc.connect('DRIVER={SQL SERVER};SERVER=tcp:facedb.database.windows.net;'
                        'DATABASE=facedb;UID=admindb;PWD=Miss@2020', autocommit=True, pooling=True)
except:
    db = pyodbc.connect('DRIVER=ODBC Driver 17 for SQL Server;SERVER=tcp:facedb.database.windows.net;'
                        'DATABASE=facedb;UID=admindb;PWD=Miss@2020', autocommit=True, pooling=True)
mycursor = db.cursor()
# db = myconectr.connect(db='admindb',user='appuser', host='facedb.database.windows.net', passwd='Miss@2020')


# myresult = mycursor.callproc(str("GetLanguageList"))
# for result in mycursor.stored_results():
#
#     myresult = result.fetchall()
# @app.post('/files')
# async def save_file():
#     file = UploadFile(...)
#     print( await file.read())
#     print("fvsklsnfklf")
#     f = open(r"C:\Users\admin\Desktop\User1.jpeg","wb")
#     f.write( await file.read())
#     print("ffdkdfm")
#     f.close()
#     return "201"

@app.on_event("startup")
@repeat_every(seconds=(24*60*60)-int(datetime.now().strftime(" %H"))*60*60-int(datetime.now().strftime(" %M"))*60-int(datetime.now().strftime(" %S")))  #time to 00:00:00
async def start():
    pass
    print((24*60*60)-int(datetime.now().strftime(" %H"))*60*60-int(datetime.now().strftime(" %M"))*60-int(datetime.now().strftime(" %S")))
    loguru.logger.add(r"/home/azureuser/file_{time:YYYY-MM-DD}.log",format="{time:YYYY-MM-DD at HH:mm:ss}   \n{message}  \n\n***************************\n\n",encoding="utf8",rotation="1 day",retention="1 week")


def log(request, x,form,fail):
    l = loguru.logger.bind()
    if str(request.query_params) != "":
        l.debug(f"{str(request.client)}  , {str(dict(request.query_params))} \n\n Answer:    {str(x)}")


@app.post('/', status_code=201)
@app.get('/')
async def index(request: Request,response: Response, j=r'{"ProjectId":"1"}', proc="getpartnersjs"):


    try:
        print(j)
        mycursor.execute('{ CALL  '+str(proc)+' (?)}', (str(j),))
        print(proc)
        myresult = mycursor.fetchall()
        x = ""
        for i in myresult:
            x += i[0]
        if str(proc).lower() == "postemailnewpassword":
            x = json.loads(str(x))
            print(x)

            x= email(x["email"],x["body"],x["subject"])


        # if '"code":"1"' in x:
        #     mycursor.execute("commit")
        #     print("534354354534")
        # if '"code":"0"' in x:
        #     mycursor.execute("rollback")
        print(x)
        log(request,json.loads(x),"{time:YYYY-MM-DD at HH:mm:ss}  oooooooooooooooo \n{message}  \n***************************\n\n",False)
        return {"data": json.loads(x)}
    except Exception as er:
        # if str(er).split(":"):
        #     er = str(er).split(":")
        #     return {
        #         "name": er[1],
        #         "message": "User session is offline",
        #         "code": er[0],
        #         "status": 401,
        #     }
        log(request,str(er),"{time:YYYY-MM-DD at HH:mm:ss}   \n{message}  \n***************************\n\n",True)
        #notifier.notify(message=str(er) , **params)
        print(str(er))
        er=str(er)
        response.status_code=400
        f=er.find("'")
        l=er.find("'",f+1)
        code=er[f+1:l]
        f=er.rfind("]")
        l=er.rfind(".")
        name=er[f+1:l]
        return {"name": name, "message": "User session is offline", "code": code}

def email(email,x,sub):

    yag = yagmail.SMTP("edf1204.f@gmail.com","=1q2w3e4r%")
    print("email is"+email)
    yag.send(
        to=email,
        subject=sub,
        contents=x,
        # attachments=filename,
    )
    return '{"code":1}'

     # try:
     #
     #     notifier.notify(message="The application is running!", **params)
     #     account_sid = 'AC9d7a5211eb4ae8f9fc07441192102d62'
     #     auth_token = '915cfa62d5a1ad3895ebbdf1f5e7dc38'
     #     client = Client(account_sid, auth_token)
     #     message = client.messages \
     #         .create(
     #         body="The application is running!",
     #         from_='+14704501886',
     #         to='+972586224916'
     #     )
     #     print(message.sid)
     # except:
     #     pass

# @app.post('/', status_code=201)
# async def add_user(j, proc):
#     try:
#         # y = [j]
#         # myresult="jh"
#         # mycursor.callproc(str(proc), args=y)
#         # for result in mycursor.stored_results():
#         #         #     myresult = result.fetchall()
#         #         # print(myresult[0][0])
#         #         #
#         #         # return {'data': json.loads(myresult[0][0])}
#         mycursor.execute('{call ' + str(proc) + '(' + str(j) + ')}')
#         myresult = mycursor.fetchall()
#         x = ""
#         for i in myresult:
#             x += i[0]
#         return {"data": json.loads(x)}
#
#     except Exception as er:
#         try:
#             er = str(er).split(":")
#             return {"name": er[1], "message": "User session is offline", "code": er[0], "status": 401}
#         except:
#             return str(er)


#tr
    #
    # @app.get('/id={id}', response_model=tuple)
    # async def index(id:int):
    #     return db[id]
    #
    #
    #
    # @app.post('/', status_code=201)
    # async def add_movie(payload: Movie):
    #     data = payload.dict()
    #     db.append(data)
    #     return {'id': len(db) - 1}
    #
    #
    # @app.put('/{id}')
    # async def update(id: int,):
    #     #data =.dict()
    #     data_length = len(db)
    #     if not(0 <= id <= data_length):
    #         raise HTTPException(status_code=404, detail="Movie with given id not found")
    #     db[id] = data
    #     return None
    #
    #
    #
    # @app.delete('/{id}')
    # async def delete(id: int):
    #     data_length = len(db)
    #     if not(0 <= id <= data_length):
    #         raise HTTPException(status_code=404, detail="Movie with given id not found")
    #     del db[id]
    #     return None
#     pass
# except Exception as e:
#     print(e)
nest_asyncio.apply()
uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
# notifier.notify(message="The application is not running!", **params)
# account_sid = 'AC9d7a5211eb4ae8f9fc07441192102d62'
# auth_token = '915cfa62d5a1ad3895ebbdf1f5e7dc38'
# client = Client(account_sid, auth_token)
# message = client.messages \
#               .create(
#               body="\n\nThe application is not running!",
#               from_='+14704501886',
#               to='+972586224916'
#           )
# print(message.sid)