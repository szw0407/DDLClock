import jsonlines
import time
import jionlp as jio
from typing import List

def nlp(log_file):
    with open(log_file, 'r+') as f:
        for item in jsonlines.Reader(f):
            content = item['message']
            try:
                print(jio.parse_time(content, time_base=time.time()))
            except:
                print("\"" + content + "\"" + " " + "have no symbol of time")

nlp("QQlog.json")






