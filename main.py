import os
from fastapi import FastAPI
import pyperclip
import uvicorn
import webbrowser
import uuid
import requests
import json

from typing import Union

from pydantic import BaseModel

import values

app = FastAPI()
# ClientID=
# RedirectURL=
# ScopeList=

tenant="common"

def ReadProfile(): 
    with open('profiles.json','r') as prof_file:
        prof=json.load(prof_file)
        global ClientID
        global RedirectURL
        global ScopeList   
        try:
            ClientID=prof["client_ID"]
            RedirectURL=prof["redirect_URL"]
            ScopeList=prof["scope"]
        except:
            print("Err:File profiles.json Error")

        # print(ClientID)
        # print(RedirectURL)
        # print(ScopeList)

@app.get("/{login}")
async def read_item(state:str,error:Union[str,None]=None,error_description:Union[str,None]=None, code:Union[str,None]=None):
    tmp={"state":state}
    # dataobj={"client_id":ClientID,"scope":ScopeList,"code":code,"redirect_uri":RedirectURL,"grant_type":"authorization_code"}
    # UUID check NOT done yet
    if state == values.get_value("UUID") or True:
        if error is not None:
            tmp.update({"error":error,"error_description":error_description})        
        elif code is not None:    
            tmp.update({"code":code})
            # ret NOT completed
            # 
            # ret = requests.post("https://login.microsoftonline.com//{tenant}/oauth2/v2.0/token",data=dataobj)
            # tmp.update(ret)
    else:
        tmp.update({"error":"state wrong"})
    
    
    return tmp

if __name__ == "__main__":
    ReadProfile()
    values.set_value("UUID",str(uuid.uuid4()))
    UUIDst=values.get_value("UUID")
    LoginURL=f"https://login.microsoftonline.com/{tenant}/oauth2/v2.0/authorize?client_id={ClientID}&response_type=code&redirect_uri={RedirectURL}&response_mode=query&scope={ScopeList}&state={UUIDst}"
    webbrowser.open(LoginURL)
    uvicorn.run("main:app", reload=True)
