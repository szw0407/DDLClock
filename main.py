from fastapi import FastAPI

import os
import uvicorn
import webbrowser
import uuid
import requests
import json

from typing import Union, Dict, List

from pydantic import BaseModel

import values
from GetPlatformInfo import show_os_info

app = FastAPI()

tenant = "common"
# used for Microsoft Account login

class GlobalDateTime(BaseModel):
    dateTime:str # YYYY-MM-DDT00:00:00
    timeZone:str = 'China Standard Time'

class DefaultMsEvent(BaseModel):
    class EventBody(BaseModel):
        contentType: str = 'HTML'
        content:str = '' # str in raw or html. e.g."<html><head><meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\"><meta name=\"Generator\" content=\"Microsoft Exchange Server\"><!-- converted from rtf --><style><!-- .EmailQuote { margin-left: 1pt; padding-left: 4pt; border-left: #800000 2px solid; } --></style></head><body><font face=\"Times New Roman\" size=\"3\"><span style=\"font-size:12pt;\"><a name=\"BM_BEGIN\"></a></span></font></body></html>"
    class loc(BaseModel):
        displayName:str
    class attendee(BaseModel):
        class emad(BaseModel):
            address:str
            name:str
        emailAddress:emad
        type:str = 'required'
    subject:str
    body:Union[EventBody,None] = None
    start:GlobalDateTime
    end:GlobalDateTime
    location:Union[None,loc] = None
    isReminderOn:Union[bool,None] = None # True default in Ms
    reminderMinutesBeforeStart:Union[int,None] = None # 15 minutes default in Ms; Minutes Ahead.
    attendees:Union[List[attendee],None] = None
    allowNewTimeProposals:Union[bool,None] = None
    transactionId:Union[None,str] = None # Maybe a UUID again, but not sure.

def ReadProfile():
    with open('config.json', 'r') as cfg_file:
        prof = json.load(cfg_file)
        cfg_file.close() # CLOSE THE FILE WHEN YOU DON'T NEED TO READ OR EDIT IT!
        try:
            prof["client_ID"]
            prof["redirect_URL"]
            prof["scope"]
            # to check whether the file include the essentials
        except:
            print("Err:File config.json Error")
            prof=None
    return prof


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
            try:
                GetToken = requests.post(f"https://login.microsoftonline.com//{tenant}//oauth2//v2.0//token",data=dataobj, headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4146.4 Safari/537.36'})
            except:
                ret={"error":"unable to get token"}
            if str(GetToken)=="<Response [200]>":
                try:
                    ret=json.loads(GetToken.text)
                except json.JSONDecodeError:
                    ret = {"error":"200 with json decode error"}
            elif str(GetToken)=="<Response [400]>":
                ret={"error":"400 Unable to get token"}
            elif ret=={"error":"unable to get token"}:
                ret=ret
            else:
                ret={"error":"Unknown Error"}

            tmp.update(ret)
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
    email=setf["email"]
    with open("token.temp","r") as tok_file:
        tokf=json.load(tok_file)
        tok_file.close()
    token=tokf["access_token"]
    NoneK=[]
    for key in data.keys():
        if data[key]==None:
            NoneK.append(key)
    for key in NoneK:
        del data[key]
    POST = requests.post(f"https://graph.microsoft.com/v1.0/me/events",data=json.dumps(data), headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4146.4 Safari/537.36',"Authorization":f"Bearer {token}","Content-Type":"application/json"})
    # return {"st":str(POST)}
    ret=data
    ret.update({"User":email,"token":token,"POST RET":str(POST)})
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
    prof=ReadProfile() #init
    sys=show_os_info(ShowAllInTerminal=True)
    print("Try to run go-cqhttp.")
    # Can only start CQ-HTTP for Windows.
    s=sys["system"]
    if s=='Windows':
        os.system("cd go-cqhttp && go-cqhttp.bat")
    elif s=='Linux':
        print("[Warn] Linux auto start is not supported now.")
        m=sys["machine"]
        if m=='AMD64' or m=='x86_64':
            print("[INFO] Linux AMD64 release deb file prepared in /go-cqhttp/LinuxRelease folder.")
            print("[INFO] To get other versions or update it, please go to https://github.com/Mrs4s/go-cqhttp/releases")
        else:
            print(f"[INFO] Linux release for {m} is available on GitHub Release.")
            a=input("Go to download it now?(y/n)")
            if a=="y" or a=="Y":
                webbrowser.open("https://github.com/Mrs4s/go-cqhttp/releases")
            else:
                print("Canceled.")
    else:
        print(f"[Warn]You are running {s}. You might need to build the file on your own to run it.")
        a=input("[Info]You may go to GitHub releases to see whether a release for {s} is available or download the source code and build it using Golang. Download now?(y/n)")
        if a=="y" or a=="Y":
            webbrowser.open("https://github.com/Mrs4s/go-cqhttp/releases")
            webbrowser.open("https://docs.go-cqhttp.org/guide/quick_start.html#%E5%A6%82%E4%BD%95%E8%87%AA%E5%B7%B1%E6%9E%84%E5%BB%BA")
        else:
            print("Canceled.")
    UUID = str(uuid.uuid4())
    temp = open(".UUID.temp", "w")
    temp.write(UUID)
    temp.close()
    #save the random UUID
    ClientID = prof["client_ID"]
    RedirectURL = prof["redirect_URL"]
    ScopeList = prof["scope"]
    LoginURL = f"https://login.microsoftonline.com/{tenant}/oauth2/v2.0/authorize?client_id={ClientID}&response_type=code&redirect_uri={RedirectURL}&response_mode=query&scope={ScopeList}&state={UUID}"
    webbrowser.open(LoginURL)
    # open the website and login
    uvicorn.run("main:app", reload=True)
