import requests
import json
def list_ddls(url,msgsq,grpid):
    ls=[]
    url=url+f"/get_group_msg_history?message_seq={msgsq}&group_id={grpid}"
    get=requests.get(url=url)
    t=get.text
    t=json.loads(t)
    t=t.get("data").get("messages")
    for i in t:
        ls.append(i.get("message"))
    return ls