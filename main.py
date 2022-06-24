import discord
from discord.ext import commands
from youtube_dl import YoutubeDL
import time
import asyncio
import bs4
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from discord.utils import get
from discord import FFmpegPCMAudio

bot = commands.Bot(command_prefix='^')
client = discord.Client()

user = [] #노래저장
musictitle = [] #노래 제목
song_queue = [] #노래 링크
musicnow = [] #지금 노래 출력

def title(msg):
    global music

    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    options = webdriver.ChromeOptions()
    options.add_argument("headless")

    chromedriver_dir = r"C:/Users/comma/OneDrive/바탕 화면/d_c/chromedriver.exe"
    driver = webdriver.Chrome(chromedriver_dir, options = options)
    driver.get("https://www.youtube.com/results?search_query="+msg+"+lyrics")
    source = driver.page_source
    bs = bs4.BeautifulSoup(source, 'lxml')
    entire = bs.find_all('a', {'id': 'video-title'})
    entireNum = entire[0]
    music = entireNum.text.strip()
    
    musictitle.append(music)
    musicnow.append(music)
    test1 = entireNum.get('href')
    url = 'https://www.youtube.com'+test1
    with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
    URL = info['formats'][0]['url']

    driver.quit()
    
    return music, URL


def play(ctx):
    global vc
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    URL = song_queue[0]
    del user[0]
    del musictitle[0]
    del song_queue[0]
    vc = get(bot.voice_clients, guild=ctx.guild)
    if not vc.is_playing():
        vc.play(FFmpegPCMAudio(URL,**FFMPEG_OPTIONS), after = lambda e:play_next(ctx))

def play_next(ctx):
    if len(musicnow) - len(user) >= 2:
        for i in range(len(musicnow) - len(user) - 1):
            del musicnow[0]
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    if len(user) >= 1:
        if not vc.is_playing():
            del musicnow[0]
            URL = song_queue[0]
            del user[0]
            del musictitle[0]
            del song_queue[0]
            vc.play(discord.FFmpegPCMAudio(URL,**FFMPEG_OPTIONS), after=lambda e: play_next(ctx))
    else:
        if not vc.is_playing():
            client.loop.create_task(vc.disconnect())

@bot.event
async def on_ready():
    print('다음으로 로그인합니다')
    print(bot.user.name)
    print('봇 작동')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("개발"))

@bot.command() #도움말
async def 도움말(ctx):
    await ctx.send(embed = discord.Embed(title="도움말", description = "^mhelp , ^음악도움말 = [음악 관련 도움말]\n추가 기능은 개발중입니다.", color = 0x00ff00))
@bot.command()
async def command(ctx):
    await ctx.send(embed = discord.Embed(title="도움말", description = "^mhelp , ^음악도움말 = [음악 관련 도움말]\n추가 기능은 개발중입니다.", color = 0x00ff00))

@bot.command() #음악 도움말
async def mhelp(ctx):
    await ctx.send(embed = discord.Embed(title="음악도움말", description = "^멜론 = [최신 멜론차트를 재생합니다.]\n ^p = [노래를 재생, 대기열에 추가합니다.]\n ^r , ^remove + 숫자 = [대기열에서 입력한 숫자의 노래를 지웁니다.]\n ^queue , ^l = [대기열을 확인합니다\n ^lreset = [대기열을 초기화 합니다.]\n^n = [현재 노래를 종료합니다]\n####아직 개발단계이기에 노래재생까지 약 10초 전후의 시간이 발생합니다####", color = 0x00ff00))

@bot.command() #음악 도움말
async def 음악도움말(ctx):
    await ctx.send(embed = discord.Embed(title="음악도움말", description = "^멜론 = [최신 멜론차트를 재생합니다.]\n ^p = [노래를 재생, 대기열에 추가합니다.]\n ^r , ^remove + 숫자 = [대기열에서 입력한 숫자의 노래를 지웁니다.]\n ^queue , ^l = [대기열을 확인합니다\n ^lreset = [대기열을 초기화 합니다.]\n^n = [현재 노래를 종료합니다]\n####아직 개발단계이기에 노래재생까지 약 10초 전후의 시간이 발생합니다####", color = 0x00ff00))

@bot.command() #영어 보이스 입장 코드
async def join(ctx):
    try:
        global vc
        vc = await ctx.message.author.voice.channel.connect()
        await ctx.send("참가 완료")
    except:
        try:
            await vc.move_to(ctx.message.author.voice.channel)
        except:
            await ctx.send("채널에 유저가 접속 해있지 않습니다")
            
@bot.command() #한글 보이스 입장 코드
async def 들어와(ctx):
    try:
        global vc
        vc = await ctx.message.author.voice.channel.connect()
        await ctx.send("참가 완료")
    except:
        try:
            await vc.move_to(ctx.message.author.voice.channel)
        except:
            await ctx.send("채널에 유저가 접속 해있지 않습니다")

@bot.command() #영어 보이스 퇴장 코드
async def leave(ctx):
    try:
        await vc.disconnect()
    except:
        await ctx.send("이미 그 채널에 속해있지 않습니다")
@bot.command() #한글 보이스 퇴장 코드
async def 나가(ctx):
    try:
        await vc.disconnect()        
    except:
        await ctx.send("이미 그 채널에 속해있지 않습니다")
        
@bot.command()
async def now(ctx):
    if not vc.is_playing():
        await ctx.send("지금은 노래가 재생되고 있지 않습니다")
    else:
        await ctx.send(embed = discord.Embed(title = "지금노래", description = "현재" + musicnow[0] + "을(를) 재생하고 있습니다.", color = 0x00ff00))

@bot.command() #최신 멜론차트 재생
async def 멜론(ctx):
    try:
        global vc
        vc = await ctx.message.author.voice.channel.connect()
        await ctx.send("참가 완료")
    except:
        try:
            await vc.move_to(ctx.message.author.voice.channel)
        except:
            await ctx.send("채널에 유저가 접속 해있지 않습니다")

    if not vc.is_playing():
        
        options = webdriver.ChromeOptions()
        options.add_argument("headless")

        global entireText
        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
            
        chromedriver_dir = r"C:/Users/comma/OneDrive/바탕 화면/d_c/chromedriver.exe"
        driver = webdriver.Chrome(chromedriver_dir, options = options)
        driver.get("https://www.youtube.com/results?search_query=멜론차트")
        source = driver.page_source
        bs = bs4.BeautifulSoup(source, 'lxml')
        entire = bs.find_all('a', {'id': 'video-title'})
        entireNum = entire[0]
        entireText = entireNum.text.strip()
        musicurl = entireNum.get('href')
        url = 'https://www.youtube.com'+musicurl 

        driver.quit()

        musicnow.insert(0, entireText)

        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        await ctx.send(embed = discord.Embed(title= "노래 재생", description = "현재 " + entireText + "을(를) 재생하고 있습니다.", color = 0x00ff00))
        vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after=lambda e: play_next(ctx))
    else:
        await ctx.send("이미 노래가 재생 중이라 노래를 재생할 수 없습니다.")

@bot.command()
async def remove(ctx, *, number):
    try:
        ex = len(musicnow) - len(user)
        del user[int(number) - 1]
        del musictitle[int(number) - 1]
        del song_queue[int(number)-1]
        del musicnow[int(number)-1+ex]
            
        await ctx.send("대기열이 정상적으로 삭제되었습니다.")
    except:
        if len(list) == 0:
            await ctx.send("대기열에 노래가 없어 삭제할 수 없어요!")
        else:
            if len(list) < int(number):
                await ctx.send("숫자의 범위가 목록개수를 벗어났습니다!")
            else:
                await ctx.send("숫자를 입력해주세요!")

@bot.command()
async def r(ctx, *, number):
    try:
        ex = len(musicnow) - len(user)
        del user[int(number) - 1]
        del musictitle[int(number) - 1]
        del song_queue[int(number)-1]
        del musicnow[int(number)-1+ex]
            
        await ctx.send("대기열이 정상적으로 삭제되었습니다.")
    except:
        if len(list) == 0:
            await ctx.send("대기열에 노래가 없어 삭제할 수 없어요!")
        else:
            if len(list) < int(number):
                await ctx.send("숫자의 범위가 목록개수를 벗어났습니다!")
            else:
                await ctx.send("숫자를 입력해주세요!")

@bot.command()
async def queue(ctx):
    if len(musictitle) == 0:
        await ctx.send("아직 아무노래도 등록하지 않았어요.")
    else:
        global Text
        Text = ""
        for i in range(len(musictitle)):
            Text = Text + "\n" + str(i + 1) + ". " + str(musictitle[i])
            
        await ctx.send(embed = discord.Embed(title= "노래목록", description = Text.strip(), color = 0x00ff00))

@bot.command()
async def l(ctx):
    if len(musictitle) == 0:
        await ctx.send("아직 아무노래도 등록하지 않았어요.")
    else:
        global Text
        Text = ""
        for i in range(len(musictitle)):
            Text = Text + "\n" + str(i + 1) + ". " + str(musictitle[i])
            
        await ctx.send(embed = discord.Embed(title= "노래목록", description = Text.strip(), color = 0x00ff00))

@bot.command()
async def lreset(ctx):
    try:
        ex = len(musicnow) - len(user)
        del user[:]
        del musictitle[:]
        del song_queue[:]
        while True:
            try:
                del musicnow[ex]
            except:
                break
        await ctx.send(embed = discord.Embed(title= "목록초기화", description = """목록이 정상적으로 초기화되었습니다. 이제 노래를 등록해볼까요?""", color = 0x00ff00))
    except:
        await ctx.send("아직 아무노래도 등록하지 않았어요.")

@bot.command()
async def plist(ctx, *, msg):
    try:
        global vc
        vc = await ctx.message.author.voice.channel.connect()
        await ctx.send("참가 완료")
    except:
        try:
            await vc.move_to(ctx.message.author.voice.channel)
        except:
            await ctx.send("채널에 유저가 접속 해있지 않습니다")

    if not vc.is_playing():

        options = webdriver.ChromeOptions()
        options.add_argument("headless")

        global entireText
        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
            
        chromedriver_dir = "C:/Users/comma/OneDrive/바탕 화면/d_c/chromedriver.exe"
        driver = webdriver.Chrome(chromedriver_dir, options = options)
        driver.get("https://www.youtube.com/results?search_query="+msg+"+lyrics")
        source = driver.page_source
        bs = bs4.BeautifulSoup(source, 'lxml')
        entire = bs.find_all('a', {'id': 'video-title'})
        entireNum = entire[0]
        entireText = entireNum.text.strip()
        musicurl = entireNum.get('href')
        url = 'https://www.youtube.com'+musicurl 

        driver.quit()

        musicnow.insert(0, entireText)

        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        await ctx.send(embed = discord.Embed(title= "노래 재생", description = "현재 " + musicnow[0] + "을(를) 재생하고 있습니다.", color = 0x00ff00))
        vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after=lambda e: play_next(ctx))

    else:
        user.append(msg)
        result, URLTEST = title(msg)
        song_queue.append(URLTEST)
        await ctx.send(result + "를 재생목록에 추가했어요!")

@bot.command()
async def n(ctx):
    if vc.is_playing():
        vc.stop()
        await ctx.send(embed = discord.Embed(title= "노래끄기", description = entireText  + "을(를) 종료했습니다.", color = 0x00ff00))
    else:
        await ctx.send("지금 노래가 재생되지 않네요.")

@bot.command()  #이스터에그
async def 이스터에그(ctx):
        await ctx.send(embed = discord.Embed(title="이스터에그", description = "사실 수철쌤은 가발을 쓰고 계신게 아니였을까?", color = 0x00ff00))

            

bot.run('OTg4NDUwOTA3MjE5OTcyMTg5.GTdMug.3PCYHCApZvwoG9R7Hvwn0sEzr5hcxzQV6nT5CY')
