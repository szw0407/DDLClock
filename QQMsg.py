import requests
import json
from __qqddl__ import *
def list_ddls(url,msgsq,grpid):
    url = f"{url}/get_group_msg_history?message_seq={msgsq}&group_id={grpid}"
    get=requests.get(url=url)
    t=get.text
    t=json.loads(t)
    t=t.get("data").get("messages")
    return [i.get("message") for i in t]