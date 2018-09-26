# menhera
基于itchat的一个自动回复  
### 使用方法：  
python3 reply.py，然后拿微信扫一扫显示的二维码  
1.  回复文本消息，使用了两个数组对是否发送消息和发送什么消息进行了判断
2.  回复语音消息，调用了ffmpeg将微信的MP3语音文件转换为wav格式，调用了百度语音api进行语音识别，并结合文本消息回复
3.  回复图片消息
4.  回复群聊消息，只有当群聊里面@本人时，才会回复
### 相关的API调用
1.[图灵机器人](www.tuling123.com)  
2.[百度语音API](http://ai.baidu.com/)
```pip install baidu-aip```
```
from aip import AipSpeech
APP_ID=''
API_KEY=''
SECRET_KEY=''
client=AipSpeech(APP_ID,API_KEY,SECRET_KEY)
```
3.ffmpeg的使用  
[ffmpeg](https://www.jianshu.com/p/7ed3be01228b)
