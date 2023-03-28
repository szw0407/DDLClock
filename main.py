from fastapi import FastAPI
import uvicorn
import os,sys
import requests
import json
import time
from typing import Union
from __qqddl__ import ddlrw
from __qqddl__.schemas import *
import sys
import jionlp as jio
from MsAPIPost import *
from StartUp import *
from nlp import nlp
import QQMsg
import subprocess
# import values
import webbrowser
from fastapi.staticfiles import StaticFiles
from fastapi.routing import Mount


app = FastAPI()
app.mount("/gui", StaticFiles(directory="dist"), name="index")

def read_settings(filename):
    with open(filename, "r") as set_file:
        setf=json.load(set_file)
        set_file.close()
        return setf # 没啥用的文件，留作备用吧
# 一个参数
tenant = "common"

def get_login_info(port:int):
    userinfo = requests.get(f"http://127.0.0.1:{port}/get_login_info")
    return json.loads(userinfo.text)
# 获得登录的QQ号

# used for Microsoft Account login
def use_api(url,data,token,preferences):
    NoneK = [key for key in data.keys() if data[key] is None]
    for key in NoneK:
        del data[key]
    
    if data.get("reminderMinutesBeforeStart") is None and preferences.get("reminderMinutesBeforeStart") is not None:
        data["reminderMinutesBeforeStart"]=preferences.get("reminderMinutesBeforeStart")
    dt=json.dumps(data)
    POST = requests.post(url,data=dt, headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4146.4 Safari/537.36',"Authorization":f"Bearer {token}","Content-Type":"application/json"})
    ret=data
    ret.update({"token":token,"POST RET":str(POST)})
    ret.update(json.loads(POST.text))
    return ret

def get_token(filename):
    """
    > If the token is expired, get a new one and save it to a temporary file. 

    :param filename: The name of the file where the token is stored
    :return: The access token is being returned.

    """
    def read_token(fn):
        with open(fn,"r") as tok_file:
            # Loading the file into a dictionary.
            tokf=json.load(tok_file)
        return tokf

    tokf=read_token(filename)
    # 如果超时重新拉取token
    if tokf["load_time"]+tokf["expires_in"]<time.time()-1:
        # The URL for getting the token.
        url=f"https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token"
        # Reading the config file and preparing the POST object for getting a new token.
        dataobj=read_config("config.json",refreshToken=tokf["refresh_token"],grantType="refresh_token")
        save_token(filename="token.temp",content=get_token_from_code(url,dataobj))
        tokf=read_token(filename)
    return tokf.get("access_token")


def read_config(filename,grantType,authoriationCode=None,refreshToken=None):
    """
    It reads the configuration file and returns a dictionary of the parameters needed to make the
    request
    
    :param filename: contains the configuration information
    :param grantType: This is the type of grant you are requesting
    :param authoriationCode: This is the code that you get from the authorization URL
    :param refreshToken: This is the token that you get when you first authenticate. You can use this to
    get a new access token
    :return: A dictionary with the client_id, scope, grant_type, refresh_token, code, and redirect_uri
    """
    with open(filename, 'r') as cfg_file:
        prof = json.load(cfg_file)
    ClientID = prof["client_ID"]
    RedirectURL = prof["redirect_URL"]
    ScopeList = prof["scope"].replace("%20"," ")
   # Preparing the POST object for getting the token.
    dataobj={"client_id":ClientID,"scope":ScopeList,"grant_type":grantType}
    if grantType=="refresh_token":
        dataobj["refresh_token"] = refreshToken
    elif grantType=="authorization_code":
        dataobj |= {"code":authoriationCode,"redirect_uri":RedirectURL}
    return dataobj


def save_token(filename,content): # 保存登录令牌
    with open(filename,"w") as f:
        # time.time返回当前时间的时间戳
        content.update({"load_time":time.time()})
        # 不转义非ASCII字符
        f.write(json.dumps(content,ensure_ascii=False))


def init(debug=False): # 初始化
    # 如果debug，打印token；如果不debug，运行gocqhttp，打印token
    if not(debug):
        p=start_gocqhttp()
        if p=="win":
            subprocess.Popen("cd go-cqhttp && go-cqhttp.exe",shell=True)
        elif p=="Linux":
            subprocess.Popen("cd ./go-cqhttp/ && ./go-cqhttp",shell=True)
    try:
        print(get_token("token.temp"))
    except Exception:
        print("No token")
    
@app.get("/login_info/")
async def get_login_info_all():
    try:
        token=get_token("token.temp")
        MsUserInfo=requests.get("https://graph.microsoft.com/v1.0/me/",headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4146.4 Safari/537.36',"Authorization":f"Bearer {token}","Content-Type":"application/json"})
        MsUserInfo=json.loads(MsUserInfo.text)
        LoginMS=True
    except Exception:
        MsURL=login(ReadProfile('config.json'), make_UUID(open(".UUID.temp", "w")))
        MsUserInfo=None
        LoginMS=False
    with open("./go-cqhttp/config.yml","r",encoding="utf-8") as f:
        p=get_cqhttp_httpserver_port(f,useWS=False)
        try:
            QQinfo=get_login_info(p[0])
            # LoginQQ=True
        except Exception:
            QQinfo={}
            # LoginQQ=False
    ret = {"MsUserInfo":MsUserInfo} if LoginMS else {"LoginMSURL":MsURL}
    ret["QQinfo"]=QQinfo.get("data")
    return ret


@app.get("/{login}")
async def read_item(state: str, error: Union[str, None] = None, error_description: Union[str, None] = None, code: Union[str, None] = None):
    """
    It reads the UUID from the file, and if the UUID matches the state, it will read the config file and
    get the token from the code
    
    :param state: The state parameter is a string that is passed back and forth between the client and
    the authorization server. It is used to maintain state between the request and the callback. This
    parameter should be used for preventing cross-site request forgery and will be passed back to you,
    unchanged, in the response
    :type state: str
    :param error: The error code
    :type error: Union[str, None]
    :param error_description: A description of the error
    :type error_description: Union[str, None]
    :param code: The authorization code returned from the initial request
    :type code: Union[str, None]
    :return: The token.
    """
    # Used when Microsoft Account Login REDIRECTS
    tmp = {"state": state}
    # 有个疑惑，下面的error是会互相覆盖的，是否可以改进
    # 读取UUID
    try:
        with open(".UUID.temp", "r") as f:
            UUID = f.read()
    except Exception:
        tmp={"error":"cannot load UUID"}
        UUID=""
    # 读取config，并把授权代码（authoriationcode)和granttype塞进同一个字典中
    try:
        dataobj=read_config(authoriationCode=code,filename='config.json',grantType="authorization_code")
    except Exception:
        tmp={"error":"cannot load Profile"}
        dataobj=None

    if state == UUID:
        if dataobj is not None:
            if error is not None:
                tmp |= {"error": error, "error_description": error_description}
            elif code is not None:
                tmp["code"] = code
                url=f"https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token"
                # 核心步骤1，获取token，可是上面为什么要update tmp
                tmp=get_token_from_code(url,dataobj)
            else:
                tmp.update({"error":"No error but no code returned"})
    elif tmp.get("error") != None:
        tmp.update({"error": "state != UUID"})
    if tmp.get("error") is None:
        try:
            # 核心步骤2，把获取到的token写入临时文件
            save_token(filename="token.temp",content=tmp)
            # It deletes the UUID file.
            if os.name=='nt':
                os.system("del -f -q .UUID.temp")
            elif os.name=='posix':
                os.system("rm -f ./.UUID.temp")
        except Exception:
            tmp.update({"error":"token UNABLE to save. Please copy the information here."})
    return tmp

@app.post("/MsCalendar")
async def create_event(data:DefaultMsEvent):
    # 一个用来测试的端口，对接微软API
    """
    It creates an event in your Outlook calendar.
    
    :param data: The data to be sent to the API
    :return: A dictionary with the following keys:
        - subject
        - body
        - bodyPreview
        - importance
        - sensitivity
        - start
        - end
        - location
        - isAllDay
        - isCancelled
        - isOrganizer
        - recurrence
        - responseRequested
        - seriesMasterId
        - show
    """
    data=data.dict()

    try:
        token=get_token("token.temp")
    except Exception:
        token=None
    with open("settings.json", "r") as set_file:
        setf=json.load(set_file)

    return use_api(
        url="https://graph.microsoft.com/v1.0/me/events",
        data=data,
        token=token,
        preferences=setf,
    )

@app.post("/QQ")
async def read_item(data: Dict):
    ls = None
    if data.get("post_type") == "message" and data.get("message_type")=="group": 
        
        try:
            res = jio.ner.extract_time(data["message"], time_base=time.time())          
        except Exception:
            print('false')
        else:
            with open("./go-cqhttp/config.yml","r",encoding="utf-8") as f:
                port=get_cqhttp_httpserver_port(f)[0]

            ls=QQMsg.list_ddls(url=f"http://127.0.0.1:{port}",grpid=data["group_id"],msgsq=data["message_seq"]) # 成功
            print(ls) # 爬取上面19条消息
        if res != [] :
                info=nlp(res,data["group_id"],data["message"])
                
                info.save_in_DB()
                
    return ls # Return anything you want in fact.

@app.put("/ddl")
async def Modify_DDL(data:Item):
    ddlrw.update_ddl(id=data.id,blog=data)
    data=ddlrw.read_item(id=data.id)
    return data


@app.post("/ddl")
async def create_DDL(data:ItemCreate):
    return ddlrw.create_item_for_group(item=data)

@app.put("/group")
async def Modify_group(data:list[GroupModify]):
    ret=[]
    for i in data:    
        ddlrw.create_group(group=i)    
        ret.append(ddlrw.read_group_by_groupnumber(i.group_number)[0])
    return ret

@app.delete("/ddl")
async def Del_DDL(id:int):
    return ddlrw.delete_ddl(id)

@app.get("/ddls/")
async def get_DDLs():
    settings=read_settings("settings.json")

    with open("./go-cqhttp/config.yml","r",encoding="utf-8") as f:
        p=get_cqhttp_httpserver_port(f)
        try:
            ret={"userInformation":get_login_info(port=p[0]).get("data")}
        except Exception:
            ret={}

    x=ddlrw.read_items()
    DDLlist=[]
    for i in x:
        x1=dict(i.__dict__)
        x1.pop("group_num")
        x1["from_group_info_all"] = ddlrw.read_group_by_groupnumber(i.group_num)
        DDLlist.append(x1)
    ret["DDL"] = DDLlist

    return ret

@app.get("/groups/")
async def get_groups():
    g={}
    with open("./go-cqhttp/config.yml","r",encoding="utf-8") as f:
        p=get_cqhttp_httpserver_port(f)        
        port=p[0]
        try:
            g=requests.get(f"http://localhost:{port}/get_group_list")
            print(g.text)
            g=json.loads(g.text)
        except Exception:
            return {}
        else:
            if g != {}:
                for i in g.get("data"):
                    QQMsg.write_group(i)
    g=ddlrw.read_groups()
    return g

if __name__ == "__main__":
    debug = bool(sys.gettrace())
    init(debug)
    if debug:
        uvicorn.run("main:app",reload = True)
    else:
        subprocess.Popen("uvicorn main:app ", shell=True)
        webbrowser.open("http://localhost:8000/gui/index.html")
    # 主进程等待一个输入
        input("Press any key to exit...")
        if os.name=='nt':
        # 输入任何字符后，终止两个子进程
            os.system("taskkill -f -im go-cqhttp.exe && taskkill -f -im uvicorn.exe")
        else:
            os.system("pkill go-cqhttp")
            os.system("pkill uvicorn")
            os.system("rm -f ./go-cqhttp/go-cqhttp")
        print("Both processes are terminated.")
