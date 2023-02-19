import re
import yaml
import webbrowser
import uuid
import json
import os

def ReadProfile(f):
    with open(f, 'r') as cfg_file:
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

def start_gocqhttp(sys):
    print("Try to run go-cqhttp.")
    # Can only start CQ-HTTP for Windows.
    s=sys["system"]
    if s=='Windows':
        os.system("cd go-cqhttp && go-cqhttp.bat")
    elif s=='Linux':
        print("[Warn] Linux auto start is not supported now.")        
        print("[INFO] Linux AMD64 release deb file prepared in /go-cqhttp/LinuxRelease folder.")
        print("[INFO] To get other versions or update it, please go to https://github.com/Mrs4s/go-cqhttp/releases")
    else:
        print(f"[Warn]You are running {s}. You might need to build the file on your own to run it.")
        print(f"[Info]You may go to GitHub releases to see whether a release for {s} is available or download the source code and build it using Golang.")
        print("Below are pages you can refer to:")
        print("https://github.com/Mrs4s/go-cqhttp/releases")
        print("https://docs.go-cqhttp.org/guide/quick_start.html#%E5%A6%82%E4%BD%95%E8%87%AA%E5%B7%B1%E6%9E%84%E5%BB%BA")
    f=None
    def get_cqhttp_httpserver_port(file):
        def get_port_number(ip_address):# bing AI 写的，反正我看不懂
            # 匹配IP地址和可选的端口号
            pattern = r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(:\d+)?"
            # 搜索字符串中的匹配项
            match = re.search(pattern, ip_address)
            if match:
                # 如果找到匹配项，返回第二个捕获组（即端口号）中的数字
                port = match.group(2)
                if port:
                    return int(port[1:]) # 去掉冒号
                else:
                    return None # 如果没有端口号，返回None
            else:
                return None # 如果没有匹配项，返回None
        port =[]
        c=file.read()
        data=yaml.load(c,Loader=yaml.FullLoader)
        servers=data.get('servers')
        
        for i in servers:
            http=i.get("http")
            k=get_port_number(http.get("address"))
            if k is not None:
                port.append(k)
        return port
    with open("./go-cqhttp/config.yml","r",encoding="utf-8") as f: 
        port=get_cqhttp_httpserver_port(f) 
        f.close()
    if port==0:
        print("Error:YAML of Go-cqhttp Error")
    print(port)
    return port
def make_UUID(temp):
    UUID = str(uuid.uuid4())    
    temp.write(UUID)
    temp.close()
    return UUID

def login(prof,UUID,debug=False):
    if prof!=None:
        ClientID = prof["client_ID"]
        RedirectURL = prof["redirect_URL"]
        ScopeList = prof["scope"]
        tenant="common"
        LoginURL = f"https://login.microsoftonline.com/{tenant}/oauth2/v2.0/authorize?client_id={ClientID}&response_type=code&redirect_uri={RedirectURL}&response_mode=query&scope={ScopeList}&state={UUID}"
        if debug:
            print(LoginURL)
        else:
            webbrowser.open(LoginURL)
    else:
        print("Error:Profile error")
