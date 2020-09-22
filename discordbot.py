


import discord
import requests
import ast
import urllib.parse
import subprocess, os
import asyncio



def loadSetting(kind):
	global gasurl
	row=31
	if kind=="cfg":
		row=32
	elif kind=="words":
		row=33
	try:
		url=gasurl+"?col=21&row=%d" % row
		response = requests.get(url)
		ret = urllib.parse.unquote(response.text)
		if ret[:3]=="ok,":
			return ret[3:]
	except Exception:
		pass
	return None

def saveSetting(kind,text):
	global gasurl
	row=31
	if kind=="cfg":
		row=32
	elif kind=="words":
		row=33
	try:
		encryptText = urllib.parse.quote("ok,"+text)
		url=gasurl+("?col=21&row=%d&txt=" % row)+encryptText
		response = requests.get(url)
		if response.status_code==200:
			return True
	except Exception:
		pass
	return False


def loadSettingDict():
	ret=loadSetting("cfg")
	if ret is None:
		return None
	try:
		return ast.literal_eval(ret)
	except Exception:
		pass
	return None

def saveSettingDict(dic):
	if type(dic) is dict:
		return saveSetting("cfg",str(dic))
	return False

def loadSettingWords():
	ret=loadSetting("words")
	if ret is None:
		return None
	try:
		return ast.literal_eval(ret)
	except Exception:
		pass
	return None

def saveSettingWords(lst):
	if type(lst) is list:
		return saveSetting("words",str(lst))
	return False

def getVoiceConfig(name):
	global cfg
	ret={}
	ret["kind"]=cfg.get(name+"_kind","")
	ret["spd"]=cfg.get(name+"_spd","")
	ret["pit"]=cfg.get(name+"_pit","")
	ret["emo"]=cfg.get(name+"_emo","")
	ret["voc"]=cfg.get(name+"_voc","")
	ret["kind"]="normal" if ret["kind"]=="" else ret["kind"]
	ret["spd"]=0.0 if ret["spd"]=="" else ret["spd"]
	ret["pit"]=0.0 if ret["pit"]=="" else ret["pit"]
	ret["emo"]=0.0 if ret["emo"]=="" else ret["emo"]
	ret["voc"]="hikari" if ret["voc"]=="" else ret["voc"]
	return ret

def convertVoiceConfig(src):
	if src["kind"]=="happy":
		src["kind"]="happiness"
	elif src["kind"]=="angry":
		src["kind"]="anger"
	elif src["kind"]=="sad":
		src["kind"]="sadness"
	if src["spd"]<0:
		src["spd"]=(50-100)/(-1-0)*(src["spd"]-0)+100
	elif src["spd"]>=0:
		src["spd"]=(400-100)/(1-0)*(src["spd"]-0)+100
	if src["pit"]<0:
		src["pit"]=(50-100)/(-1-0)*(src["pit"]-0)+100
	elif src["pit"]>=0:
		src["pit"]=(200-100)/(1-0)*(src["pit"]-0)+100
	if src["emo"]<-0.4:
		src["emo"]=1
	elif src["emo"]<0.4:
		src["emo"]=2
	elif src["emo"]<0.8:
		src["emo"]=3
	else:
		src["emo"]=4






token = os.environ['DISCORD_BOT_TOKEN']
vtoken = os.environ['VOICETEXT_API_TOKEN']
gasurl = os.environ['GAS_URL']


cfg=loadSettingDict()
if cfg is not None:
	print("successfully loaded")
	print(cfg)
else:
	print("failed to load")
	cfg={}

words=loadSettingWords()
if words is not None:
	print("successfully loaded")
	print(words)
else:
	print("failed to load")
	words=[]


if not discord.opus.is_loaded():
	discord.opus.load_opus("/app/.heroku/vendor/lib/libopus.so");

client = discord.Client()

connected=False
voicecnt=0

def procWord(txt, bAuthorName):
	global words
	if bAuthorName==False:
		bW=False
		ret=""
		for i in range(0,len(txt)):
			if txt[i]=="w" or txt[i]=="W" or txt[i]=="ｗ" or txt[i]=="Ｗ":
				if bW==False:
					if i==len(txt)-1 or txt[i+1]=="\r" or txt[i+1]=="\n" or \
					   txt[i+1]=="\t" or txt[i+1]==" " or txt[i+1]=="　" or \
					   txt[i+1]=="w" or txt[i+1]=="W" or txt[i+1]=="ｗ" or txt[i+1]=="Ｗ":
						ret+="。わら。"
						bW=True
					else:
						ret+=txt[i]
						bW=False
				else:
					pass
			else:
				ret+=txt[i]
				bW=False
		txt=ret
	for i in words:
		if i[0]!="":
			oword=i[0]
			if oword[0]=="!":
				if bAuthorName==False:
					continue
				oword=oword[1:]
			txt=txt.replace(oword,i[1])
	return txt

async def on_message_connect(message):
	global connected
	if message.author.voice is None or message.author.voice.channel is None:
		await message.channel.send("> [DEBUG] あなたはボイスチャンネルに接続していません。")
		return
	# ボイスチャンネルに接続する
	await message.author.voice.channel.connect()
	await message.channel.send("> へぃ！ぃらっしゃい！")
	connected=True
async def on_message_disconnect(message):
	global connected
	if message.guild.voice_client is None:
		await message.channel.send("> [DEBUG] 接続されていません。")
		return
	# 切断する
	await message.guild.voice_client.disconnect()
	await message.channel.send("> またのご来店お待ちぇしゃせぃ！")
	connected=False


@client.event
async def on_message(message):
	global connected, voicecnt,cfg,words
	
	# ignore bot msg
	if message.author.bot and cfg.get("readbot","0")=="0":
		return
	
	if message.content[0] == '/':
		pass
	elif message.content[0] == '$':
		pass
	elif message.content[0] == '?':
		pass
	elif message.content[0] == ';':
		pass
	elif message.content[0] == '!':
		m=message.content[1:]
		m=m.replace("　"," ")
		m=m.replace("\t"," ")
		v=m.split(" ")
		if v[0].lower() == 'oqn' and len(v)>=2:
			v2=m.split(" ",1)
			await message.channel.send('[DEBUG] !OQN: ' + v2[1])
		if v[0].lower() == 'oqd' and len(v)>=2:
			v2=m.split(" ",1)
			proc = subprocess.run(v2[1].split(),stdout = subprocess.PIPE, stderr = subprocess.PIPE)
			await message.channel.send(proc.stdout.decode("utf8"))
		if v[0].lower() == 'oqs':
			await on_message_connect(message)
		if v[0].lower() == 'oqe':
			await on_message_disconnect(message)
		if v[0].lower() == 'oq' and len(v)>=2:
			if v[1].lower()=="s":
				await on_message_connect(message)
			if v[1].lower() == 'e':
				await on_message_disconnect(message)
			if v[1].lower() == 'uv':
				if len(v)<5:
					await message.channel.send("> [DEBUG] 構文エラー")
					return
				if v[2] not in ["normal","happy","angry","sad"]:
					await message.channel.send("> [DEBUG] 構文エラー: %s" % v[2])
					return
				if v[2] == "bashful":
					await message.channel.send("> [DEBUG] ささやき声bashfulは未サポートです。")
					return
				if len(v)>=7 and v[6] not in ["haruka","hikari","takeru","santa","bear"]:
					await message.channel.send("> [DEBUG] 構文エラー: %s" % v[6])
					return
				try:
					v[3]=float(v[3])
				except Exception:
					v[3]=0.0
				v[3]=-1 if v[3]<-1 else v[3]
				v[3]=1 if v[3]>1 else v[3]
				try:
					v[4]=float(v[4])
				except Exception:
					v[4]=0.0
				v[4]=-1 if v[4]<-1 else v[4]
				v[4]=1 if v[4]>1 else v[4]
				if len(v)>=6:
					try:
						v[5]=float(v[5])
					except Exception:
						v[5]=0.0
					v[5]=-1 if v[5]<-1 else v[5]
					v[5]=1 if v[5]>1 else v[5]
				#
				cfg[message.author.name+"_kind"]=v[2]
				cfg[message.author.name+"_spd"]=v[3]
				cfg[message.author.name+"_pit"]=v[4]
				if len(v)>=6:
					cfg[message.author.name+"_emo"]=v[5]
				if len(v)>=7:
					cfg[message.author.name+"_voc"]=v[6]
				await message.channel.send("> あいよ！声設定一丁！")
				ret=saveSettingDict(cfg)
				if ret == True:
					#print("successfully saved")
					pass
				else:
					await message.channel.send("> [DEBUG] ネットワークエラー。設定値の保存に失敗")
			if v[1].lower() == 'gv':
				vcfg=getVoiceConfig(message.author.name)
				msg=""
				msg += "> 声の種別：%s\n" % vcfg["kind"]
				msg += "> 喋る速さ：%s\n" % str(vcfg["spd"])
				msg += "> 声の高さ：%s\n" % str(vcfg["pit"])
				if vcfg["kind"]!="normal":
					msg += "> 感情強さ：%s\n" % str(vcfg["emo"])
				else:
					msg += "> 感情強さ：0\n"
				msg += "> 声優種類：%s\n" % vcfg["voc"]
				await message.channel.send(msg)
			if v[1].lower() == 'aw':
				if len(v)!=4:
					await message.channel.send("> [DEBUG] 構文エラー")
					return
				v[2]=v[2].strip()
				v[3]=v[3].strip()
				found=False
				for i in range(0,len(words)):
					if words[i][0]==v[2]:
						words[i][1]=v[3]
						found=True
						break
				if found==False:
					words.append([v[2],v[3]])
				words = sorted(words, key=lambda x: -len(x[0]))
				ret=saveSettingWords(words)
				if ret==True:
					await message.channel.send("> あいよ！単語登録一丁！")
				else:
					await message.channel.send("> [DEBUG] ネットワークエラー。設定値の保存に失敗")
			if v[1].lower() == 'dw':
				if len(v)!=3:
					await message.channel.send("> [DEBUG] 構文エラー")
					return
				found=False
				for i in range(0,len(words)):
					if words[i][0]==v[2].strip():
						words.pop(i)
						found=True
						break
				if found==False:
					await message.channel.send("> 単語見つかんねぇよ！")
				else:
					ret=saveSettingWords(words)
					if ret==True:
						await message.channel.send("> 単語削除一丁あがり！")
					else:
						await message.channel.send("> [DEBUG] ネットワークエラー。設定値の保存に失敗")
			if v[1].lower() == 'read_name':
				if len(v)!=3:
					await message.channel.send("> [DEBUG] 構文エラー")
					return
				if v[2].lower()=="off":
					cfg["readname"]="0"
				elif v[2].lower()=="on":
					cfg["readname"]="1"
				else:
					await message.channel.send("> [DEBUG] 構文エラー")
					return
				ret=saveSettingDict(cfg)
				if ret == True:
					await message.channel.send("> あいよ！名前読み上げ設定一丁！")
				else:
					await message.channel.send("> [DEBUG] ネットワークエラー。設定値の保存に失敗")
			if v[1].lower() == 'read_bot':
				if len(v)!=3:
					await message.channel.send("> [DEBUG] 構文エラー")
					return
				if v[2].lower()=="off":
					cfg["readbot"]="0"
				elif v[2].lower()=="on":
					cfg["readbot"]="1"
				else:
					await message.channel.send("> [DEBUG] 構文エラー")
					return
				ret=saveSettingDict(cfg)
				if ret == True:
					await message.channel.send("> あいよ！bot読み上げ設定一丁！")
				else:
					await message.channel.send("> [DEBUG] ネットワークエラー。設定値の保存に失敗")
			if v[1].lower() == 'read_limit':
				if len(v)!=3:
					await message.channel.send("> [DEBUG] 構文エラー")
					return
				num=-1
				try:
					num=int(v[2])
				except Exception:
					pass
				if 0<=num and num<10:
					num=10
				cfg["readlimit"]=num
				ret=saveSettingDict(cfg)
				if ret == True:
					await message.channel.send("> あいよ！読み上げ文字数設定一丁！")
				else:
					await message.channel.send("> [DEBUG] ネットワークエラー。設定値の保存に失敗")
	else:
		if connected:
			voice_client = message.guild.voice_client
			if not voice_client:
				await message.channel.send("> [DEBUG] Botはこのサーバーのボイスチャンネルに参加していません。")
				return
			try:
				fname="/tmp/test%d.ogg" % voicecnt
				vcfg=getVoiceConfig(message.author.name)
				convertVoiceConfig(vcfg)
				url = 'https://api.voicetext.jp/v1/tts'
				authmsg=procWord(message.author.name,True)+"。"
				if cfg.get("readname","0")=="0":
					authmsg=""
				readlimit=cfg.get("readlimit",-1)
				mainmsg=procWord(message.content,False)
				if readlimit>=0 and readlimit<len(mainmsg):
					mainmsg=mainmsg[:readlimit]+"。以下略"
				Parameters = {
					'text': authmsg+mainmsg,
					'speaker': vcfg["voc"],
					'pitch': str(int(vcfg["pit"])),
					'speed': str(int(vcfg["spd"])),
					'format': "ogg",
				}
				if vcfg["kind"]!="normal":
					Parameters["emotion"]=vcfg["kind"]
					Parameters["emotion_level"]=str(int(vcfg["emo"]))
				print(Parameters)
				
				voicecnt+=1
				if voicecnt>=100:
					voicecnt=0
				send = requests.post(url, params = Parameters, auth = (vtoken,''))
				result = open(fname, 'wb')
				result.write(send.content)
				result.close()
				
				for i in range(0,30):
					if voice_client.is_playing()==False:
						break
					await asyncio.sleep(1)
				
				ffmpeg_audio_source = discord.FFmpegPCMAudio(fname)
				voice_client.play(ffmpeg_audio_source)
				#await message.channel.send("再生しました。")
				print("[DEBUG] played")
			except Exception as e:
				await message.channel.send("> [DEBUG] 例外発生しました。%s" % e.args)

client.run(os.environ['DISCORD_BOT_TOKEN'])










