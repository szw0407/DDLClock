# 关于获取QQ的信息

目前`main.py`已经能实时记录QQ信息到那个`QQlog.json`里面了。其实没有必要实时获取，“接收到消息”的PUSH，可以用来激活、调用“同步消息记录”。

## 关于获得消息记录：

首先获得端口号，连接到cqhttp

我没想折腾websocket，如果能搞最好，看起来更省事。

下面是http requests的实现：

``` Python
with open("\\go-cqhttp\\config.yml","r") as f: # open语句的r代表读取，w代表（默认）从头写入，a代表从尾巴写入。记得路径里面的转义字符
    port=get_cqhttp_httpserver_port(f) # 这个函数可能不太好写
    # 如果那个函数写不出来就指定比如return 12000（我用的这个数字），保证和yml文件一致即可。
    # 获得服务器端口信息
    f.close() # 千万记得关闭文件！！我给坑过！！

# https://docs.go-cqhttp.org/api/#%E8%8E%B7%E5%8F%96%E7%BE%A4%E6%B6%88%E6%81%AF%E5%8E%86%E5%8F%B2%E8%AE%B0%E5%BD%95 参考这个：

url=f"127.0.0.1:{port}/get_group_msg_history"

params={
    "group_id": 1919810
    "message_seq": 114514 # 这个参数可以不加，完成第一次查询后就能得到一些序号，然后再查最早的序号得到更早的消息，后面补充进来
}
# 抄个UA
headers = {'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)'}
p=requests.get(url,params=params,headers=headers)


```

也可以先指定端口再写入yml文件，同样不太好做到。

为了省事，可以存一个文件或者写入数据库“XXX号信息已经看过了，下次不用再看了”。

先写这么多
