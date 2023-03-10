from fastapi import FastAPI
import os
import uvicorn
import requests
import json
import time
from typing import Union
import sys
import jionlp as jio


from MsAPIPost import *
from StartUp import *
from nlp import nlp
# import values

app = FastAPI()

def read_settings(filename):
    with open(filename, "r") as set_file:
        setf=json.load(set_file)
        set_file.close()
        return setf
# 一个参数
tenant = "common"

def get_login_info(port):
    userinfo = requests.get(f"http://127.0.0.1:{port}/get_login_info")
    return userinfo.text
# 获得登录的QQ号

# used for Microsoft Account login
def use_api(url,data,token):
    NoneK=[]
    for key in data.keys():
        if data[key]==None:
            NoneK.append(key)
    for key in NoneK:
        del data[key]
    POST = requests.post(url,data=json.dumps(data), headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4146.4 Safari/537.36',"Authorization":f"Bearer {token}","Content-Type":"application/json"})
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
        tok_file=open(fn,"r")
        # Loading the file into a dictionary.
        tokf=json.load(tok_file)
        tok_file.close()
        return tokf
    tokf=read_token(filename)    
    # 如果超时重新拉取token
    if tokf["load_time"]+tokf["expires_in"]<time.time():
        # The URL for getting the token.
        url=f"https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token"
        # Reading the config file and preparing the POST object for getting a new token.
        dataobj=read_config("config.json",refreshToken=tokf["refresh_token"],grantType="refresh_token")
        save_token(filename="token.temp",content=get_token_from_code(url,dataobj))
        tokf=read_token(filename)
    return tokf["access_token"]


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
    cfg_file=open(filename, 'r')
    prof = json.load(cfg_file)
    cfg_file.close()
    ClientID = prof["client_ID"]
    RedirectURL = prof["redirect_URL"]
    ScopeList = prof["scope"].replace("%20"," ")
   # Preparing the POST object for getting the token.
    dataobj={"client_id":ClientID,"scope":ScopeList,"grant_type":grantType}
    if grantType=="refresh_token":
        dataobj.update({"refresh_token":refreshToken})
    elif grantType=="authorization_code":
        dataobj.update({"code":authoriationCode,"redirect_uri":RedirectURL})
    return dataobj


def save_token(filename,content): # 保存登录令牌
    f=open(filename,"w")
    # time.time返回当前时间的时间戳
    content.update({"load_time":time.time()})
    # 不转义非ASCII字符
    f.write(json.dumps(content,ensure_ascii=False))
    f.close()


def init(debug=False): # 初始化
    # 如果debug，打印token；如果不debug，运行gocqhttp，打印token
    if not(debug):
        start_gocqhttp()
        try:
            print(get_token("token.temp"))
        except:           
            login(ReadProfile('config.json'),make_UUID(open(".UUID.temp", "w")),debug=debug)

    else:
        try:   
            print(get_token("token.temp"))
        except:
            pass
    
            

@app.get("/{login}")
# error是参数
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
        f = open(".UUID.temp", "r")
        UUID = f.read()
        f.close()
    except:
        tmp={"error":"cannot load UUID"}
        UUID=""
    # 读取config，并把授权代码（authoriationcode)和granttype塞进同一个字典中
    try:
        dataobj=read_config(authoriationCode=code,filename='config.json',grantType="authorization_code")
        # to prepare GetToken POST object
    except:
        tmp={"error":"cannot load Profile"}
        dataobj=None

    if state == UUID:
        if dataobj is not None:
            if error is not None:
                tmp.update({"error": error, "error_description": error_description})
            elif code is not None:
                tmp.update({"code": code}) # 这一行是没用的吧
                url=f"https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token"
                # 核心步骤1，获取token，可是上面为什么要update tmp
                tmp=get_token_from_code(url,dataobj)
            else:
                tmp.update({"error":"No error but no code returned"})
    else:
        try:
            tmp["error"]
        except:
            tmp.update({"error": "state != UUID"})
    try:
        tmp["error"] # If it has any errors above, do not write down!
    except:
        try:
            # 核心步骤2，把获取到的token写入临时文件
            save_token(filename="token.temp",content=tmp)
            # It deletes the UUID file.
            if os.name=='nt':
                os.system("del -f -q .UUID.temp")
            elif os.name=='posix':
                os.system("rm -f ./.UUID.temp")
        except:
            tmp.update({"error":"token UNABLE to save. Please copy the information here."})
            # The browser shows the information too.
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
    with open("settings.json", "r") as set_file:
        setf=json.load(set_file)
        set_file.close()
    try:       
        token=get_token("token.temp")
    except:
        token=None

    ret=use_api(url="https://graph.microsoft.com/v1.0/me/events",data=data.dict(),token=token)
    
    return ret # login-success.html

@app.post("/QQ")
async def read_item(data: Dict):
    k = True
    if data["post_type"] == "message" : 
        while k:
            try:
                s=json.dumps(data, ensure_ascii=False)
                t=json.loads(s)
                res = jio.ner.extract_time(s, time_base=time.time())
                if res != [] and t["message_type"]=="group" :
                    nlp(res,t["group_id"],t["message"])
                    # f = open("QQlog-utf8.json", "ab")
                    # f.write((s + "\n").encode('utf-8')) # 记录日志。
                    # # 此处是解析信息，从data取相关的内容
                    # f.close()            
            except:
                k = False
                print('false')
            else:
                k = False # 成功
    return {"Sta": "OK"} # Return anything you want in fact.
    
@app.get("/DDLs")
async def get_DDLs():
    settings=read_settings("settings.json")
    with open("./go-cqhttp/config.yml","r",encoding="utf-8") as f: 
        ret={"userInformation":get_login_info(port=get_cqhttp_httpserver_port(f))}
        f.close()
    DDLlist=[]
    # get DDLs from SQL 此处是下一个要做的事情
    ret.update({"DDL":DDLlist})
    return ret

if __name__ == "__main__":
    init(debug=True if sys.gettrace() else False)
    uvicorn.run("main:app", reload=True)
