from aip import AipSpeech
from mp32wav import mp32wav

APP_ID=''
API_KEY=''
SECRET_KEY=''

client=AipSpeech(APP_ID,API_KEY,SECRET_KEY)

def get_file_content(filepath):
	with open(filepath,'rb') as fp:
		return fp.read()
def get_result(filepath):
	filepath_r=mp32wav(filepath)
	print(filepath_r)
	m=client.asr(get_file_content(filepath_r),'pcm',8000,{'dev_pid':1537,})
	print(m)
	if 'result' in m.keys():
		return m['result']
	else:
		return 'menhera can not recognize the voice'
	print(m['result'])