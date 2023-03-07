from typing import List

class Time_msg(object):
    def __init__(self,group,text,type,time,content):
        self.__group = group
        self.__text = text
        self.__type = type
        self.__time = time
        self.__content = content

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

    



def nlp(data:List,group,content):
    for dt in data:
        try:
            gr = group
            tx = dt["text"]
            tp = dt["type"]
            t = dt["detail"]["time"]
            t_msg = Time_msg(gr,tx,tp,t,content)

            print(t_msg)
        except:
            print("error")









