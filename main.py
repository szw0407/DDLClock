from fastapi import FastAPI

import os
import uvicorn

import requests
import json

from typing import Union
from MsAPIPost import *
from StartUp import *
# import values
from GetPlatformInfo import show_os_info

app = FastAPI()

tenant = "common"
# used for Microsoft Account login

def get_token(filename):
    tok_file=open(filename,"r")
    tokf=json.load(tok_file)
    tok_file.close()
    return tokf["access_token"]

def init(debug=False):
    port=start_gocqhttp(show_os_info(ShowAllInTerminal=False))
    try:
        get_token("token.temp")
    except:
        login(ReadProfile('config.json'),make_UUID(open(".UUID.temp", "w")),debug=debug)

@app.get("/{login}")
async def read_item(state: str, error: Union[str, None] = None, error_description: Union[str, None] = None, code: Union[str, None] = None):
    # Used when Microsoft Account Login REDIRECTS
    tmp = {"state": state}
    try:
        f = open(".UUID.temp", "r")
        UUID = f.read()
        f.close()
    except:
        tmp={"error":"cannot load UUID"}
        UUID=""
    try:
        cfg_file=open('config.json', 'r')
        prof = json.load(cfg_file)
        cfg_file.close()
        ClientID = prof["client_ID"]
        RedirectURL = prof["redirect_URL"]
        ScopeList = prof["scope"].replace("%20"," ")
        dataobj={"client_id":ClientID,"scope":ScopeList,"code":code,"redirect_uri":RedirectURL,"grant_type":"authorization_code"}
        # to prepare GetToken POST object
    except:
        tmp={"error":"cannot load Profile"}
        dataobj=None

    if state == UUID and dataobj is not None:
        if error is not None:
            tmp.update({"error": error, "error_description": error_description})
        elif code is not None:
            tmp.update({"code": code})
            url=f"https://login.microsoftonline.com//{tenant}//oauth2//v2.0//token"
            
            tmp.update(get_token_from_code(url,dataobj))
    else:
        try:
            tmp["error"]
        except:
            tmp.update({"error": "state != UUID"})
    try:
        tmp["error"] # If it has any errors above, do not write down!
    except:
        try:
            f=open("token.temp","w")
            f.write(json.dumps(tmp,ensure_ascii=False))
            f.close()
            if os.name=='nt':
                os.system("del -f -q .UUID.temp")
            elif os.name=='posix':
                os.name("rm -f .UUID.temp")
        except:
            tmp.update({"error":"token UNABLE to save. Please copy the information here."})
            # The browser shows the information too.
    return tmp

@app.post("/MsCalendar")
async def create_event(data:DefaultMsEvent):
    data=data.dict()
    with open("settings.json", "r") as set_file:
        setf=json.load(set_file)
        set_file.close()
    try:       
        token=get_token("token.temp")
    except:
        token=None
    NoneK=[]
    for key in data.keys():
        if data[key]==None:
            NoneK.append(key)
    for key in NoneK:
        del data[key]
    POST = requests.post(f"https://graph.microsoft.com/v1.0/me/events",data=json.dumps(data), headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4146.4 Safari/537.36',"Authorization":f"Bearer {token}","Content-Type":"application/json"})
    # return {"st":str(POST)}
    ret=data
    ret.update({"token":token,"POST RET":str(POST)})
    ret.update(json.loads(POST.text))
    return ret

@app.post("/QQ")
async def read_item(data: Dict):
    k = 1
    if data["post_type"] != "meta_event":
        while k == 1:
            try:
                f = open("QQlog.json", "a")
                f.write(json.dumps(data, ensure_ascii=False) + ",\n")
                f.close()
            except:
                k = 1
            else:
                k = 0
    return {"Sta": "OK"} # Return anything you want in fact.
   
if __name__ == "__main__":
    init(debug=False)
    # open the website and login
    uvicorn.run("main:app", reload=True)
