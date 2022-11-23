# botress.py
import os
import json
import asyncio

from discord import FFmpegPCMAudio, PCMVolumeTransformer
from discord.ext import commands
import discord

import random

import PySimpleGUI as sg
import tkinter
import threading
import subprocess

with open("./config.json") as config_file:
  data = json.load(config_file)


#----------------------------------------------------------------------------------------------------------------------------------------

# variable initialisation
BotToken = data["token"]
returnHaButtress = ["Botress", "botress", "bottress", "Ha", "buttress", "ha", "Ha!", "ha!", "Ha! Botress.", "Ha! Buttress."]
playlistsCatagories = []
songQueue = []
global audioCount
global audioLength
global playingSong
global volumeChange
global currentSongSource
global voiceGlobal
global currentSongAddress

# prepare bot to accept commands and enable intents 
bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), intents= discord.Intents.all())

#----------------------------------------------------------------------------------------------------------------------------------------

# bot startup function
@bot.event
async def on_ready():
  # get playlist names from Music Assets folder and add them to playlistCatagories
    playlistFolder = 'MusicAssets\\'
    for song in os.listdir(playlistFolder):
      playlistsCatagories.append(song)

    print(f'\n')
    print(f'{bot.user} is in bloom!')
    print(f'\n')
    bot.loop.create_task(uiControl())
    
# bot responds to messages (and any commands which don't have their own function)
@bot.event
async def on_message(message):
  
  if message.author == bot.user:
         return

  for buttress in returnHaButtress:
        if (message.content == buttress):
          await message.channel.send('Ha! Buttress.') 
      
  if message.content == '!stop':
      await bot.close() 

  for playlistName in playlistsCatagories:
    if message.content == "!" + playlistName:
      ctx = await bot.get_context(message)
      command = bot.get_command('playlist')
      await ctx.invoke(command, playlistName)
  

  await bot.process_commands(message)

# default bot command for !playlist <insert playlist name> to start playlist in the same voice channel as the commander
@bot.command(pass_context = True)
async def playlist (ctx, playlistName):
  if (ctx.author.voice):
    try:
      voiceClient = discord.utils.get(bot.voice_clients)
      await voiceClient.disconnect()
    except:
      print("Wasn't connected")
    channel = ctx.message.author.voice.channel
    voice = await channel.connect()

    playlistFolder = 'MusicAssets\\' + playlistName
    print(playlistFolder)
    for song in os.listdir(playlistFolder):
      songPath = os.path.join(playlistFolder, song)
      if os.path.isfile(songPath):
        songQueue.append(songPath)
        print(song + " added")
   
    songNum = 0
    random.shuffle(songQueue)
    print(songQueue)
    while True:
      if not voice.is_playing():
        source = FFmpegPCMAudio(songQueue[songNum])
        print (songQueue[songNum])
        voice.play(FFmpegPCMAudio(source))
        songNum = songNum + 1
        if songNum == len(songQueue):
          songNum = 0
          random.shuffle(songQueue)   
      await asyncio.sleep(1)    
  else:
    await ctx.send("User must be in a voice channel")  

# default bot command for !leave, for the bot to leave its voice channel
@bot.command(pass_context = True)
async def leave (ctx):
  if (ctx.voice_client):
    await ctx.guild.voice_client.disconnect()
    await ctx.send("Botress makes like a tree... and leaves")
  else:
    await ctx.send("It's too late! Botress has already ingrained its roots and it's not going anywhere.")


#----------------------------------------------------------------------------------------------------------------------------------------


# UI function to start the playlist which has been clicked in the UI
async def playlistNoCtx(inputVoiceID, currentPlaylist):
        songQueue = []
        audioLength = "200"
        # try:
        #   voiceClient = discord.utils.get(bot.voice_clients)
        #   await voiceClient.disconnect()
        # except:
        #   print("Wasn't connected")
       
        if (str.isdigit(inputVoiceID)):
          integerVoiceID = int (inputVoiceID)
          voiceChannel = bot.get_channel(integerVoiceID)
        try:  
          channel = voiceChannel
          voice = await channel.connect()
        except:
          print("Already connected")
          voice = discord.utils.get(bot.voice_clients)

        playlistFolder = 'MusicAssets\\' + currentPlaylist
        print(playlistFolder)
        for song in os.listdir(playlistFolder):
          songPath = os.path.join(playlistFolder, song)
          if os.path.isfile(songPath):
            songQueue.append(songPath)
            print(song + " added")

        songNum = 0
        random.shuffle(songQueue)
        print(songQueue)
       # if not voice.is_playing():
        source = FFmpegPCMAudio(songQueue[songNum])
        global currentSongSource
        global volumeChange
        global currentSongAddress
        currentSongSource = source
        currentSongAddress = songQueue[songNum]
        print (songQueue[songNum])

        cmd = ["ffprobe", "-i", songQueue[songNum], "-show_entries", "format=duration",
        "-v", "quiet", "-of", "csv=p=0"]
        audioLength = subprocess.check_output(cmd).decode("utf-8").strip()
        if voice.is_playing():
          voice.stop()
        voice.play(source)
        voice.source = PCMVolumeTransformer(currentSongSource, volume = volumeChange)
        #   songNum = songNum + 1
        #   if songNum == len(songQueue):
        #     songNum = 0
        #     random.shuffle(songQueue)
        # else:
        #   await asyncio.sleep(1)
        # await asyncio.sleep(1)  
        
        return audioLength, voice
        

async def printHello():
  print("Hello")

# UI function to create the window and listen for clicks
async def uiControl():
  global currentSongSource
  global voiceGlobal
  global volumeChange
  volumeChange = 50 / 100
  playingSong = False
  audioLength = "200"
  audioCount = int(float(audioLength))
  JoinedVC = False
  
  sg.theme('Dark Purple 4')
  layout = [
    [sg.Text(text ="BOTRESS CONTROL PANEL", size = (20,2), auto_size_text=True, font="Impact", text_color= "Purple")],
    [sg.Text("Enter voice channel ID"), sg.InputText(key="inputVoiceID"), sg.Button("Join VC", key="joinVCButton")],
    [sg.Button(descriptions) for descriptions in playlistsCatagories[0: 9]],
    [sg.Button(descriptions) for descriptions in playlistsCatagories[9: 18]],
    [sg.Button(descriptions) for descriptions in playlistsCatagories[18: 27]],
    [sg.Button(descriptions) for descriptions in playlistsCatagories[36: 45]],
    [sg.Button(descriptions) for descriptions in playlistsCatagories[45: 54]],
    [sg.Button(descriptions) for descriptions in playlistsCatagories[54: 63]],
    [sg.Button(descriptions) for descriptions in playlistsCatagories[63: 72]],
    [sg.Button(descriptions) for descriptions in playlistsCatagories[72: 81]],
    [sg.Button(descriptions) for descriptions in playlistsCatagories[81: 90]],
    [sg.Button(descriptions) for descriptions in playlistsCatagories[90: 99]],
    [sg.Button(descriptions) for descriptions in playlistsCatagories[99: 108]],
    [],
    [sg.Text(text = "Time left on current song"), sg.Button("No song playing currently", key = "songElapsed"), sg.Button("Skip")],
    [],
    [sg.Text(text = "Volume"), sg.Slider(key = "volumeSlider", range = (0,100), default_value = 50, size = (50,20), orientation = "horizontal", enable_events = True)],
    [sg.Button("<-", key = "volumeDown"), sg.Button("->", key = "volumeUp"), sg.InputText(key = "inputVolume", size = (5,2)), sg.Button("Set Volume", key = 'volumeButton')]        
    ]
  icon = "ArtAssets\\icon.ico"
  window = sg.Window(title ="Botress Trunk", 
                    layout = layout,
                    icon = icon,
                    margins= (20,20),
                    location = (700,400),
                    finalize = True)  
  # window[canvas].bind('<FocusOut>', '+FOCUS OUT+')
  # sg.Canvas[window].bind('<Enter>', await printHello)                                            

  # UI loop to listen              
  # count = 0
  

  while True:
   
    # if count < 100:
    eventGUI, valuesGUI = window.read(timeout = 500)
   
    #   count = count + 1
    # else:
    #   await asyncio.sleep(1)
    #   count = 0
    
    # if eventGUI is None:
    #   await asyncio.sleep(1)

    # UI button event for joining voice chat
    if eventGUI == "joinVCButton":

      for resetColour in playlistsCatagories:
              window[resetColour].update(button_color = ("#382039"))
      playingSong = False
      audioLength = "200"
      audioCount = int(float(audioLength))
      window["songElapsed"].update("No song playing currently", button_color = "#382039")


      inputVoiceID = valuesGUI['inputVoiceID']
      if (str.isdigit(inputVoiceID)):
        integerVoiceID = int (inputVoiceID)
        voiceChannel = bot.get_channel(integerVoiceID)
        if voiceChannel:
          try:
            voiceClient = discord.utils.get(bot.voice_clients)
            await voiceClient.disconnect()
          except:
            print("Wasn't connected")
          await voiceChannel.connect()
          window['joinVCButton'].update(text = "VC Joined", button_color = ("Dark Green"))
          JoinedVC = True
          playingSong = False
        else:
          window['joinVCButton'].update(text = "Failed to join VC", button_color = ("Dark Red"))
      else:
        window['joinVCButton'].update(text = "Not a valid ID number", button_color = ("Dark Red"))
      
    # UI button event for selecting playlist
    for descriptions in playlistsCatagories:
      # print(window['joinVCButton'].__getattribute__("button_color"))
      if eventGUI == descriptions:
        inputVoiceID = valuesGUI['inputVoiceID']
        if JoinedVC == False:
        #if inputVoiceID == "" or not (str.isdigit(inputVoiceID)):
          window['joinVCButton'].update(text = "Please enter VC channel ID first", button_color = ("Dark Red"))
        else:
          for resetColour in playlistsCatagories:
            window[resetColour].update(button_color = ("#382039"))
          window[descriptions].update(button_color = ("Dark Green"))
          currentPlaylist = descriptions
          audioLength, voiceGlobal = await playlistNoCtx(inputVoiceID, currentPlaylist)
          playingSong = True
          audioCount = int(float(audioLength))
          audioCount = int(audioCount - (audioCount/10))
          break

    if eventGUI == "volumeSlider":
      if (playingSong):
        volumeChange = valuesGUI['volumeSlider'] / 100
        #command = 'ffmpeg -i "' + currentSongAddress + '" -af "volume="' + str(volumeChange) + " -c:v copy -c:a libmp3lame -b:a 192k output.mp3"
        #subprocess.run(command, shell = True)
        # voiceGlobal.source = PCMVolumeTransformer(currentSongSource, volume = volumeChange)

    if eventGUI == "volumeButton":
      if (playingSong):
        if int(valuesGUI['inputVolume']) <= 100:
          window['volumeButton'].update(text = "Set Volume", button_color = "#382039")
          volumeChange =  float(valuesGUI['inputVolume']) / 100
          window['volumeSlider'].update(value = volumeChange * 100)
          window.refresh()
        else: 
          window['volumeButton'].update(text = "Please enter a volume lower than 100", button_color = "Dark Red")

    if eventGUI == "volumeUp":
      if (playingSong):
        if int(valuesGUI['volumeSlider']) < 100:
          volumeChange = volumeChange + 0.01
          window['volumeSlider'].update(value = float(valuesGUI['volumeSlider']) + 1) 
          window.refresh() 

    if eventGUI == "volumeDown":
      if (playingSong):
        if int(valuesGUI['volumeSlider']) > 0:
          volumeChange = volumeChange - 0.01
          window['volumeSlider'].update(value = float(valuesGUI['volumeSlider']) - 1)
          window.refresh()

    # UI button event closing the window, breaking the loop, and closing the program
    if eventGUI == sg.WIN_CLOSED:
      break

    # countdown for time elapsed during the current song  
    if audioCount >= 0 and playingSong:
      window["songElapsed"].update(text = str(audioCount), button_color = "Dark Green")
      audioCount -= 1
      await asyncio.sleep(1)
     
    # once the current song is finished, call the playlistNoCtx function again to play a random song from the same playlist
    if (audioCount < 0 and playingSong) or (eventGUI == "Skip" and JoinedVC == True and playingSong):
      audioLength, voiceGlobal = await playlistNoCtx(inputVoiceID, currentPlaylist)
      playingSong = True
      audioCount = int(float(audioLength)) 
      audioCount = int(audioCount - (audioCount/10)) 
    
      
  # end event processing
  window.close()
  await bot.close()   


# preset command for bot event loop (note - could be removed later for greater loop/threading control)
bot.run(BotToken)
