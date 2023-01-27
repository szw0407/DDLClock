from fastapi import FastAPI

import uvicorn
import webbrowser
import uuid
import requests
import json

from typing import Union, Dict

from pydantic import BaseModel

import values

app = FastAPI()
# ClientID=
# RedirectURL=
# ScopeList=

tenant = "common"


class cqhttp_post(BaseModel):
    time: int
    self_id: int
    post_type: str
    message_type: str
    sub_type: str


def ReadProfile():
    with open('config.json', 'r') as cfg_file:
        prof = json.load(cfg_file)

        cfg_file.close()
        try:
            prof["client_ID"]
            prof["redirect_URL"]
            prof["scope"]
        except:
            print("Err:File config.json Error")
            prof=None
    return prof


@app.get("/{login}")
async def read_item(state: str, error: Union[str, None] = None, error_description: Union[str, None] = None,
                    code: Union[str, None] = None):
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
    except:
        tmp={"error":"cannot load Profile"}
        dataobj=None
    # UUID check NOT done yet

    if state == UUID and dataobj is not None:
        if error is not None:
            tmp.update({"error": error, "error_description": error_description})
        elif code is not None:
            tmp.update({"code": code})

            # ret NOT completed
            #
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
        tmp["error"]
    except:
        try:
            f=open("token.temp","w")
            f.write(json.dumps(tmp,ensure_ascii=False))
            f.close()
        except:
            tmp.update({"error":"token UNABLE to save. Please copy the information here."})
    return tmp


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
    return {"Sta": "OK"}


if __name__ == "__main__":
    prof=ReadProfile()
    UUID = str(uuid.uuid4())
    temp = open(".UUID.temp", "w")
    temp.write(UUID)
    temp.close()
    ClientID = prof["client_ID"]
    RedirectURL = prof["redirect_URL"]
    ScopeList = prof["scope"]
    LoginURL = f"https://login.microsoftonline.com/{tenant}/oauth2/v2.0/authorize?client_id={ClientID}&response_type=code&redirect_uri={RedirectURL}&response_mode=query&scope={ScopeList}&state={UUID}"
    webbrowser.open(LoginURL)
    uvicorn.run("main:app", reload=True)
