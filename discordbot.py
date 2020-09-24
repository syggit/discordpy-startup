


import discord
import requests
import ast
import urllib.parse
import subprocess, os
import asyncio
from PIL import Image, ImageDraw, ImageFont
#import math
import datetime


def makeTablePic(fontfile, output):
	tbl=[]
	cw=[]
	ch=[]
	gray=(210,210,210)
	white=(255,255,255)
	black=(0,0,0,255)
	yellow=(255,192,128,255)
	blue=(128,192,255,255)
	green=(128,255,128,255)
	#
	row=[]
	ch.append(50)
	cw.append(120)
	row.append(["",black,gray,0,0,0])   #label, forecolor, bgcolor, offsetx, offsety, font-kind
	cw.append(3)
	row.append(["",black,gray,0,0,0])
	for i in sch["date"]:
		cw.append(75)
		v=i.split("/")
		if len(v)==3:
			str="%s/%s"%(v[1],v[2])
		else:
			str=i
		if len(str)<5:
			str=" "+str
		row.append([str,black,gray,1,7,0])
	tbl.append(row)
	#
	row=[]
	ch.append(3)
	row.append(["",black,gray,0,0,0])
	row.append(["",black,gray,0,0,0])
	for i in sch["date"]:
		row.append(["",black,gray,0,0,0])
	tbl.append(row)
	#
	for j in sch["mem"]:
		row=[]
		ch.append(50)
		row.append([j,black,gray,5,7,0])
		row.append(["",black,gray,0,0,0])
		for i in sch["date"]:
			val=sch["ans"].get(j+"_"+i, 0)
			if val==2:
				row.append(["○",green,white,13,-10,1])
			elif val==1:
				row.append(["△",yellow,white,13,-10,1])
			elif val==-1:
				row.append(["×",gray,white,15,-30,2])
			else:
				row.append(["",black,white,12,2,1])
		tbl.append(row)
	
	tblx1=10
	tbly1=70
	tblx2gap=10
	tbly2gap=170
	
	tblx2=tblx1+sum(cw)
	tbly2=tbly1+sum(ch)
		
	
	im=Image.new('RGB', (tblx2+tblx2gap,tbly2+tbly2gap),(255,255,255))
	draw=ImageDraw.Draw(im)
	#fnt=ImageFont.truetype("/system/fonts/DroidSans.ttf",24)
	fnt=ImageFont.truetype(fontfile,24) #"/system/fonts/NotoSansCJK-Regular.ttc",24)
	fnt2=ImageFont.truetype(fontfile,50) #"/system/fonts/NotoSansCJK-Regular.ttc",24)
	fnt3=ImageFont.truetype(fontfile,70) #"/system/fonts/NotoSansCJK-Regular.ttc",24)
	fnt4=ImageFont.truetype(fontfile,32) #"/system/fonts/NotoSansCJK-Regular.ttc",24)
	fnt5=ImageFont.truetype(fontfile,20) #"/system/fonts/NotoSansCJK-Regular.ttc",24)
	
	y=tbly1
	for j in range(0,len(ch)):
		x=tblx1
		for i in range(0,len(cw)):
			draw.rectangle((x,y,x+cw[i],y+ch[j]),fill=tbl[j][i][2])
			x+=cw[i]
		y+=ch[j]
	
	x=tblx1
	for i in range(0,len(cw)):
		draw.line(( x,tbly1,x,tbly2),fill=(0,0,0,255),width=1)
		x+=cw[i]
	y=tbly1
	for j in range(0,len(ch)):
		draw.line(( tblx1,y,tblx2,y),fill=(0,0,0,255),width=1)
		y+=ch[j]
	draw.rectangle((tblx1-0,tbly1-0,tblx2+0,tbly2+0),outline=(0,0,0,255))
	draw.rectangle((tblx1-1,tbly1-1,tblx2+1,tbly2+1),outline=(0,0,0,255))
	draw.rectangle((tblx1-2,tbly1-2,tblx2+2,tbly2+2),outline=(0,0,0,255))
	draw.line((tblx1, tbly1,tblx1+cw[0],tbly1+ch[0]),fill=(0,0,0,255),width=1)
	
	y=tbly1
	for j in range(0,len(ch)):
		x=tblx1
		for i in range(0,len(cw)):
			draw.text((x+tbl[j][i][3],y+tbl[j][i][4]),tbl[j][i][0], \
							font=(fnt if tbl[j][i][5]==0 else (fnt2 if tbl[j][i][5]==1 else fnt3)),fill=tbl[j][i][1])
			#draw.rectangle((x,y,x+cw[i],y+ch[j]),fill=tbl[j][i][2])
			x+=cw[i]
		y+=ch[j]
		
	draw.text((5,5),sch.get("title",""),font=fnt4,fill=black)
	
	sa=[]
	sb=[]
	sa.append("＜コマンド例＞") ; sb.append("")
	sa.append("・!oq ss 1/1") ; sb.append("…　1月1日を○にする")
	sa.append("・!oq ss 1/1-1/3 1/5") ; sb.append("…　1月1日～3日と5日を○にする")
	sa.append("・!oq ss 1/1-1/3n") ; sb.append("…　1月1日～3日を×にする")
	sa.append("・!oq ss 1/1-1/3?") ; sb.append("…　1月1日～3日を△にする")
	sa.append("・!oq ss 1/1-1/3*") ; sb.append("…　1月1日～3日を空白にする")
	sa.append("・!oq ss ally") ; sb.append("…　全日程○にする（allnなら×、all?なら△）")
	for i in range(0,len(sa)):
		draw.text((5,tbly2+5+20*i),sa[i],font=fnt5,fill=black)
		draw.text((220,tbly2+5+20*i),sb[i],font=fnt5,fill=black)
	im.save(output)  #"./test.png"

def normalizeDate(lst,maxdate=30):
	ret=[]
	today = datetime.date.today()
	ty = today.year
	tm=today.month
	td=today.day
	for i in lst:
		flag=2
		if i[-1].lower()=="y":
			flag=2
			i=i[:-1]
		elif i[-1].lower()=="?":
			flag=1
			i=i[:-1]
		elif i[-1].lower()=="*":
			flag=0
			i=i[:-1]
		elif i[-1].lower()=="n":
			flag=-1
			i=i[:-1]
		v=i.split("-")
		if len(v)==1:
			v.append(v[0])
		a=v[0].split("/")
		b=v[1].split("/")
		for i in range(0,len(a)):
			try:
				a[i]=int(a[i])
			except Exception:
				raise Exception("非数値が含まれています。")
		for i in range(0,len(b)):
			try:
				b[i]=int(b[i])
			except Exception:
				raise Exception("非数値が含まれています。")
		if len(a)==1:
			a.insert(0,tm)
		if len(a)==2:
			a.insert(0,ty)
		if len(b)==1:
			if a[2]>b[0]:
				b.insert(0,a[1]+1)
			else:
				b.insert(0,a[1])
			if b[0]>12:
				b[0]=1
				b.insert(0,a[0]+1)
		if len(b)==2:
			if a[1]*31+a[2]>b[0]*31+b[1]:
				b.insert(0,a[0]+1)
			else:
				b.insert(0,a[0])
		if (a[0]*12+a[1])*31+a[2]>(b[0]*12+b[1])*31+b[2]:
				raise Exception("開始日と終了日が逆")
		try:
			ta = datetime.datetime(a[0],a[1],a[2])
			tb = datetime.datetime(b[0],b[1],b[2])
		except Exception:
			raise Exception("日付が異常です")
		cnt=0
		#print("%d/%d/%d"%(tb.year,tb.month,tb.day))
		while True:
			if cnt>maxdate:
				raise Exception("候補日数が多すぎです")
			ret.append(["%d/%d/%d"%(ta.year,ta.month,ta.day),flag])
			#print("%d/%d/%d"%(ta.year,ta.month,ta.day))
			if ta.year==tb.year and ta.month==tb.month and ta.day==tb.day:
				break
			ta=ta + datetime.timedelta(days=1)
			cnt+=1
		#
		#ret.append(["%d/%d/%d"%(a[0],a[1],a[2]),"%d/%d/%d"%(b[0],b[1],b[2])])
	return ret
def datesort(x):
	v=x.split("/")
	if len(v)!=3:
		return (9999*12+12)*31+31
	for i in range(0,len(v)):
			try:
				v[i]=int(v[i])
			except Exception:
				return (9999*12+12)*31+31
	return (v[0]*12+v[1])*31+v[2]

def findFont():
	for i in os.listdir(path='.'):
		sdir=os.path.join(".", i)
		if os.path.isdir(sdir):
			for j in os.listdir(path=sdir):
				if j[-4:].lower()==".ttf":
					return os.path.join(sdir,j)
	return ""

def loadSetting(kind):
	global gasurl
	row=31
	if kind=="cfg":
		row=32
	elif kind=="words":
		row=33
	elif kind=="sch":
		row=34
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
	elif kind=="sch":
		row=34
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

def loadSettingSchedule():
	ret=loadSetting("sch")
	if ret is None:
		return None
	try:
		return ast.literal_eval(ret)
	except Exception:
		pass
	return None

def saveSettingSchedule(dic):
	if type(dic) is dict:
		return saveSetting("sch",str(dic))
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

sch=loadSettingSchedule()
if sch is not None:
	print("successfully loaded(sch)")
	print(sch)
else:
	print("failed to load")
	sch={}
if "mem" not in sch:
	sch["mem"]=[]
if "date" not in sch:
	sch["date"]=[]
if "ans" not in sch:
	sch["ans"]={}


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
			if v[1].lower() == 'sc':
				if len(v)!=2:
					await message.channel.send("> [DEBUG] 構文エラー")
					return
				#find font
				"""
				fontfile=findFont()
				
				if fontfile=="":
					send = requests.get("https://osdn.net/frs/redir.php?m=ymu&f=mplus-fonts%2F62344%2Fmplus-TESTFLIGHT-063a.tar.xz")
					result = open("font.tar.xz", 'wb')
					result.write(send.content)
					result.close()
					proc = subprocess.run("xz -dc font.tar.xz | tar xfv -", shell=True)
					fontfile=findFont()
				if fontfile=="":
					await message.channel.send("> [DEBUG] フォント初期化エラー")
					return
				"""
				fontfile="mplus-1p-regular.ttf"
				print(fontfile)
				try:
					makeTablePic(fontfile,"/tmp/test.png")
					file_img = discord.File("/tmp/test.png")
					await message.channel.send(file=file_img)
				except Exception as e:
					await message.channel.send("> [DEBUG] 例外発生しました。%s" % str(e.args))

				#await client.send_file(message.channel, "/tmp/test.png")
			if v[1].lower() == 'sm':
				if len(v)<=2:
					await message.channel.send("> [DEBUG] 構文エラー")
					return
				elif len(v)==3 and v[2].lower()=="clear":
					sch["mem"]=[]
					msg="> あいよ！メンバー消去一丁！"
				else:
					for i in v[2:]:
						sch["mem"].append(i)
					msg="> あいよ！メンバー追加一丁！"
				ret=saveSettingSchedule(sch)
				if ret == True:
					await message.channel.send(msg)
				else:
					await message.channel.send("> [DEBUG] ネットワークエラー。設定値の保存に失敗")
				#await message.channel.send(msg)
			if v[1].lower() == 'st':
				v2=m.split(" ",2)
				if len(v2)<=2:
					await message.channel.send("> [DEBUG] 構文エラー")
					return
				sch["title"]=v2[2]
				msg="> あいよ！タイトル設定一丁！"
				ret=saveSettingSchedule(sch)
				if ret == True:
					await message.channel.send(msg)
				else:
					await message.channel.send("> [DEBUG] ネットワークエラー。設定値の保存に失敗")
				#await message.channel.send(msg)
			if v[1].lower() == 'sd':
				if len(v)<=2:
					await message.channel.send("> [DEBUG] 構文エラー")
					return
				elif len(v)==3 and v[2].lower()=="clear":
					sch["date"]=[]
					msg="> あいよ！日付消去一丁！"
				else:
					try:
						ret=normalizeDate(v[2:])
						for i in ret:
							if i[0] not in sch["date"]:
								sch["date"].append(i[0])
						if len(sch["date"])<=30:
							msg="> あいよ！日付追加一丁！"
						else:
							sch["date"]=sch["date"][:30]
							msg="> あいよ！日付追加一丁！(候補日数30件超えたため切り捨てました)"
						sch["date"] = sorted(sch["date"], key=datesort)
					except Exception as e:
						msg="> [DEBUG] 例外発生しました(sd)：%s" % e.args
				ret=saveSettingSchedule(sch)
				if ret == True:
					await message.channel.send(msg)
				else:
					await message.channel.send("> [DEBUG] ネットワークエラー。設定値の保存に失敗")
				#await message.channel.send(msg)
			if v[1].lower() == 'ss':
				if len(v)<=2:
					await message.channel.send("> [DEBUG] 構文エラー")
					return
				elif len(v)==3 and v[2].lower()=="clear":
					sch["ans"]={}
					msg="> あいよ！全スケジュール消去一丁！"
				elif len(v)==3 and v[2].lower()=="clearall":
					sch["ans"]={}
					sch["date"]=[]
					msg="> あいよ！全スケジュールと日付消去一丁！"
				elif len(v)==3 and (v[2].lower()=="ally" or v[2].lower()=="alln" or v[2].lower()=="all?" or v[2].lower()=="all*"):
					flag=None
					if v[2].lower()=="ally":
						flag=2
					elif v[2].lower()=="alln":
						flag=-1
					elif v[2].lower()=="all?":
						flag=1
					elif v[2].lower()=="all*":
						flag=0
					if flag is None:
						msg="> [DEBUG] 例外発生しました。%s" % e.args
					else:
						for i in sch["date"]:
							sch["ans"][message.author.name+"_"+i]=flag
						msg="> あいよ！日付全件の設定完了！"
				else:
					try:
						sindex=2
						target=message.author.name
						if len(v)>=4 and v[2] in sch["mem"]:
							target=v[2]
							sindex=3
						ret=normalizeDate(v[sindex:],400)
						cnt=0
						for i in ret:
							if i[0] in sch["date"]:
								sch["ans"][target+"_"+i[0]]=i[1]
								cnt+=1
						if cnt==0:
							msg="> [DEBUG] 候補日以外の日付が指定された可能性があります。"
						else:
							msg="> あいよ！ %d 件の設定完了！" % cnt
					except Exception as e:
						msg="> [DEBUG] 例外発生しました(ss)：%s" % e.args
				ret=saveSettingSchedule(sch)
				if ret == True:
					await message.channel.send(msg)
				else:
					await message.channel.send("> [DEBUG] ネットワークエラー。設定値の保存に失敗")
				#await message.channel.send(msg)
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










