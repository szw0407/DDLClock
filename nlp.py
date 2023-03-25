from typing import List
from __qqddl__.schemas import ItemCreate
from __qqddl__ import ddlrw
# from datetime import
class Time_msg:
    __group__:str =""
    __text__:str=""
    __time__ = ""
    __type__=""
    __content__=""
    def __init__(self,group,text,type,time,content):
        self.__group__ = str(group)
        self.__text__ = text
        self.__type__ = type
        self.__time__ = time[1] if time[1] != "inf" else time[0]
        self.__content__ = content
    def save_in_DB(self):
        return ddlrw.create_item_for_group(item=ItemCreate(text=self.__content__,
                                                           ddltime=self.__time__,
                                                           status="",
                                                           group_num=self.__group__,
                                                           description=self.__text__)
                                                           )
    # def get_group(self):
    #     return self.__group
    # def get_type(self):
    #     return self.__type
    
    # def get_text(self):
    #     return self.__text
    
    # def get_time(self):
    #     return self.__time
    
    # def get_content(self):
    #     return self.__content
    
    # def set_group(self,group):
    #     self.__group = group
    
    # def set_type(self, type):
    #     self.__type = type

    # def set_text(self, text):
    #     self.__text = text

    # def set_time(self, time):
    #     self.__time = time

    # def set_content(self, content):
    #     self.__content = content

    



def nlp(data:List,group,content:str):
    for dt in data:
        try:
            gr = group
            tx = f"{content[:19]}..."
            tp = dt["type"]
            
            t = [i.replace(" ","T",1) for i in dt["detail"]["time"]]
            return Time_msg(gr,tx,tp,t,content)
        except Exception:
            print("error")
            return "error"



