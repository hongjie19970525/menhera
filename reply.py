#coding=utf-8

'''menhera酱是基于itchat进行了二次开发的一个小东西，满足了本人对于二次元人物的憧憬
1.回复文本消息，使用了两个数组对是否发送消息和发送什么消息进行了判断
2.回复语音消息，调用了ffmpeg将微信的MP3语音文件转换为wav格式，调用了百度语音api进行语音识别，并结合文本消息回复
3.回复图片消息，
4.回复群聊消息，只有当群聊里面@本人时，才会回复
'''

import itchat   					#调用了itchat模块，具体请看https://github.com/littlecodersh/ItChat
import requests
import random
from recog import get_result
from mp32wav import mp32wav
key='' 								#自己申请的key
Re=False
Re_pic=True							#全局变量name[]存储发送者的ID，name_re[]存储回复了exit的ID
name=[]
name_re=[]

'''tuling_reply()是调用了tuling123的api，传入msg的信息，接收到返回来的文本信息后，再return出去'''
def tuling_reply(msg):
	apiurl='http://www.tuling123.com/openapi/api'
	data={
		'key':key,
		'info':msg,
		'userid':'wechat-robot',
		}
	try:
		r=requests.post(apiurl,data=data).json()
		return r.get('text')
	except:
		return '不好意思，menhera酱也要睡觉啦'  #为了防止调用的时候出现异常导致程序中断，使用try-except

'''normal_reply()是用户第一次发送信息时的回复'''		
def normal_reply(msg):
	return 'Hello,'+msg+'，menhera酱来啦！(回复“聊天”即可进入聊天模式,回复“退出”即可退出聊天模式，回复exit退出自动应答，回复enter进入自动应答)'

	
@itchat.msg_register(itchat.content.PICTURE)                                                
def reply(msg):
	global Re_pic
	N=random.randint(1,120)															'''图片是随机发的，自己用的时候要配置好图片文件夹目录，review下来感觉Re_pic跟name冲突了'''
	if (msg['FromUserName'] not in name):
		itchat.send_image('./pic/'+str(N)+'.jpg',toUserName=msg['FromUserName'])
		name.append(msg['FromUserName'])
		Re_pic=True
		return 
	if (msg['FromUserName'] in name and Re_pic==True):		
		itchat.send_image('./pic/'+str(N)+'.jpg',toUserName=msg['FromUserName'])
	
@itchat.msg_register(itchat.content.RECORDING)										
def reply(msg):
	print(msg['FileName'])
	msg_rec=msg['Text']('./Record/'+msg['FileName'])#首先把语音文件下载到本地上，然后通过mp32wav函数将MP3格式转换为wav格式，在getresult函数里调用了百度API，返回来的字符串通过tuling_reply()函数再回传回回复消息
	print(msg_rec)
	print(type(msg['FileName']))
	print(msg['FileName'])
	itchat.send_msg(msg=tuling_reply(get_result(msg['FileName'])),toUserName=msg['FromUserName'])
	
@itchat.msg_register(itchat.content.TEXT,isGroupChat=True)
def reply(msg):
	if(msg.isAt):
		print(msg['Text'])
		msg=msg['Text'].split('丶',1)[1]			#这里我调用了split函数对文本消息进行切割，也就是@草莓丶，取丶的后半部分，如果没有消息的话printenter，但是这个分支总是进不去，布置到为什么
		print(msg)
		if msg==None:
			print('enter')
			return '来自menhera酱的回复：收到'
		else:
		
			return tuling_reply(msg)	

@itchat.msg_register(itchat.content.TEXT)
def reply(msg):
	global Re#这里是引用全局变量，而不是定义全局变量
	global name
	global name_re
	global Re_no                                                                                                                    '''这部分的逻辑结构太混乱了，我已经不想碰这部分了'''
	if msg['FromUserName'] not in name and msg['Text']!='聊天' and msg['FromUserName'] not in name_re and msg['Text']!='exit':
		print(type(msg['User']['RemarkName']))
		print(msg['User']['RemarkName'])

		return normal_reply(msg['User']['RemarkName'])
	if msg['FromUserName'] not in name_re and msg['Text']=='exit' and msg['FromUserName'] not in name:
		name_re.append(msg['FromUserName'])
		print('success')
		return
	if msg['FromUserName'] not in name and msg['Text']=='聊天' and msg['FromUserName'] not in name_re:
		Re=True
		name.append(msg['FromUserName'])
		return '聊天开始'
	if msg['FromUserName'] in name and Re==True and msg['Text']!='退出' and msg['FromUserName'] not in name_re:
		return tuling_reply(msg['Text'])
	if msg['FromUserName'] in name and msg['Text']=='退出' and msg['FromUserName'] not in name_re:
		name.remove(msg['FromUserName'])
		return '再见'
	if msg['FromUserName'] in name_re and msg['Text']=='enter' and msg['FromUserName'] not in name:
		name_re.remove(msg['FromUserName'])
		return normal_reply()

itchat.auto_login(enableCmdQR=True,hotReload=True)		
itchat.run()

