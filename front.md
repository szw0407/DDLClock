# 和前端交互

1. 前端请求体：GET`localhost:8000/DDLs`

返回前端的数据：

```javascript
Data = {
        "userInformation": "114514"
            // {
            //     "avatarAddress": "../user1/avatar1.jpg" 
            // }, 

        "ddl":   
            [
                {
                    "id":1
                    "ddlContent": "一起去保卫萝卜",  
                    "date": "2022-06-08T22:12:32",   
                    "group": "保卫萝卜二群",  
                    "rank": "不紧急", 
                    "src": "经研究，本群决定于2022年6月8日22时12分32秒，与大家一起去保卫萝卜，收到请回复！" 
                },
                ······
            ],

        "ddlGroups": 
            [
                {  
                    "groupName": "保卫萝卜二群", 
                    "status": true
                }, 
                ······
            ]

        }
```

2. 前端登录

`localhost:8000/qq_login`

返回：

`filelike PNG`

3. 前端返回更新 POST`localhost:8000/DDLs`

4. 用户头像：`localhost`
