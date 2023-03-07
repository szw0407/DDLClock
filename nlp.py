from typing import List

from sql_app import ddlrw
class Time_msg:
    __group__=0
    __text__=""
    __time__="2006-01-02T15:04:05"
    __type__=""
    __content__=""
    def __init__(self,group,text,type,time,content):
        self.__group__ = group
        self.__text__ = text
        self.__type__ = type
        self.__time__ = time
        self.__content__ = content

    # def get_group(self):
    #     return self.__group
    def record(self):
        ddlrw.create_item_for_user()
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

    



def nlp(data:List,group,content):
    for dt in data:
        try:
            gr = group
            tx = dt["text"]
            tp = dt["type"]
            t = dt["detail"]["time"]
            t_msg = Time_msg(gr,tx,tp,t,content)

            return t_msg
        except:
            print("error")
            return "error"








