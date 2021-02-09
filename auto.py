from __future__ import unicode_literals
from bs4 import BeautifulSoup
import requests
import json
import youtube_dl
import ffmpeg
import discord
import string
import random
import os

def main():
    # Starts Discord Client
    client = discord.Client()

    # Converts config.Json into dictionary
    config = open("config.json", "r")
    keys = json.loads(config.read())

    @client.event
    async def on_ready():
        print("Process is ready!")

    @client.event
    async def on_voice_state_update(member, before, after):
        # Checks that it is my client who joined
        if member == client.user and after.channel != before.channel and after.channel != None:

                word = ''

                # Picks 5 Random Letters for Search Query
                for x in range(5):
                    word += random.choice(string.ascii_letters)

                # Prepares Api Call
                url = 'https://www.googleapis.com/youtube/v3/search?key=' + keys["youtubeKey"] + "&maxResults=1&part=snippet&type=video&q="+word

                # Makes Api Call & Scrapes Json Reply
                page = requests.get(url).json()

                # Grabs Video ID
                videoID = page['items'][0]['id']['videoId']

                # Prepares Youtube-DL
                youtubeVideo = {
                    'format': 'bestaudio/best',
                    'outtmpl': 'video.mp3',
                    'noplaylist': 'True',
                }

                # Downloads the Youtube Video
                with youtube_dl.YoutubeDL(youtubeVideo) as ydl:
                    ydl.download(["https://www.youtube.com/watch?v=" + videoID])

                # FFMPEG handles cutting clip down to five seconds
                stream = ffmpeg.input('video.mp3', t=5)
                stream = ffmpeg.output(stream, 'output.mp3')
                ffmpeg.run(stream)

                # Grabs Bot-Chat Channel
                channel = client.get_channel(558932672634945537)
            
                # Uploads the MP3 to the Bot Chat Channel
                with open('output.mp3', 'rb') as fp:
                    await channel.send("/im -s", file=discord.File(fp, 'output.mp3'))

                # Deletes both files when completed
                if os.path.exists('video.mp3'):
                    os.remove('video.mp3')

                if os.path.exists('output.mp3'):
                    os.remove('output.mp3')

    # Starts the bot up
    client.run(keys["discordKey"], bot=False)

if __name__ == "__main__":
    main()