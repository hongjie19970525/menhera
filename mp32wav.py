import os
import subprocess
 
def mp32wav(filename):

	subprocess.call(['ffmpeg/bin/ffmpeg','-i','./Record/'+filename,'./newrecord/'+filename.split('.')[0]+'.wav'])   #设置好ffmpeg的文件路径
	return './newrecord/'+filename.split('.')[0]+'.wav'


